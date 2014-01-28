import re
import requests
import reversion

from bs4 import BeautifulSoup
from datetime import datetime
from django.db import transaction

from .base import HtmlSoupParser
from ..models import HaaretzArticle, HaaretzImage
from ..utils import get_file_from_url


class HaaretzParser(HtmlSoupParser):

    BASE_URL = 'http://www.haaretz.co.il'
    HOMEPAGE_URL = BASE_URL + '/'
    ARTICLE_HREF_PATTERN = re.compile(r'''^(http:\/\/www\.haaretz\.co\.il)?/((news|opinions|magazine|captain)/[a-zA-Z0-9\-\/]*(\.premium-)?)?1\.\d+(#article_comments)?$''')
    ARTICLE_ID_PATTERN = re.compile(r'1\.\d+')
    ARTICLE_MODEL = HaaretzArticle
    IMAGE_MODEL = HaaretzImage

    def article_id_to_url(self, article_id):
        return '{}/{}'.format(self.BASE_URL, article_id)

    def parse_article(self, url, soup):
        haaretz_id = re.findall(self.ARTICLE_ID_PATTERN, url)[0]
        title = soup.find('h1', class_='mainTitle').text.strip()
        subtitle = soup.find('h2', class_='subtitle').text.strip()
        author_bar = soup.find('ul', class_='author-bar')
        author = author_bar.find(class_=re.compile('autorBar(Anchor|Writers)')).text.strip()
        date = author_bar.find_all('li')[1].text.strip()
        time = author_bar.find_all('li')[2].text.strip()
        article_date = self.TIMEZONE.localize(datetime.strptime(' '.join([date, time]), '%d.%m.%Y %H:%M'))
        article_body = soup.find('div', id='article-box').find_all('p')
        article_text = '\n\n'.join([p.text.strip() for p in article_body])

        with transaction.atomic(), reversion.create_revision():
            try:
                existing_article = self.ARTICLE_MODEL.objects.get(haaretz_id=haaretz_id)
                changed = False
                if title != existing_article.title:
                    existing_article.title = title
                    changed = True
                if subtitle != existing_article.subtitle:
                    existing_article.subtitle = subtitle
                    changed = True
                if article_text != existing_article.text:
                    existing_article.text = article_text
                    changed = True
                if changed:
                    existing_article.save()
            except self.ARTICLE_MODEL.DoesNotExist:
                article = self.ARTICLE_MODEL(url=url, haaretz_id=haaretz_id, title=title,
                    subtitle=subtitle, author=author, text=article_text, date=article_date)
                article.save()

                images = soup.find('div', id='article-box').find_all('div', class_='inArticleHoldImage')
                for image in images:
                    img = image.find('img')
                    img_url = 'http://www.haaretz.co.il{}'.format(img['src'].split('_gen')[0])
                    caption = img.title

                    name, image_file = get_file_from_url(img_url)

                    article_image, created = self.IMAGE_MODEL.objects.get_or_create(origin_url=img_url,
                        defaults={'article': article, 'caption': caption})

                    if created:
                        article_image.image.save(name, image_file)
                        article_image.save()
                        
                        # from ..tasks import preload_thumbnail
                        # preload_thumbnail.delay(article_image.image.url, '150x120')

    def clean_article_href(self, href):
        href = href.replace('.premium-', '').split('#')[0]
        return super(HaaretzParser, self).clean_article_href(href)
