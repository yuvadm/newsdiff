import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime

from .base import HtmlSoupParser
from ..models import HaaretzArticle, HaaretzImage
from ..utils import get_file_from_url


class HaaretzParser(HtmlSoupParser):

    HOMEPAGE_URL = 'http://www.haaretz.co.il/'
    ARTICLE_HREF_PATTERN = re.compile(r'''^(http:\/\/www\.haaretz\.co\.il)?/((news|opinions|magazine|captain)/[a-zA-Z0-9\-\/]*(\.premium-)?)?\d\.\d+(#article_comments)?$''')
    ARTICLE_MODEL = HaaretzArticle
    IMAGE_MODEL = HaaretzImage

    def parse_homepage(self, soup):
        links = soup.find_all('a', href=self.ARTICLE_HREF_PATTERN)
        hrefs = [link['href'] for link in links]
        article_urls = list(set(map(self.clean_article_href, hrefs)))
        return article_urls

    def parse_article(self, haaretz_id, soup, url=None):
        if not url:
            url = 'http://www.haaretz.co.il/{}'.format(haaretz_id)
        title = soup.find('h1', class_='mainTitle').text.strip()
        subtitle = soup.find('h2', class_='subtitle').text.strip()
        author_bar = soup.find('ul', class_='author-bar')
        date = author_bar.find_all('li')[1].text.strip()
        time = author_bar.find_all('li')[2].text.strip()
        article_date = self.TIMEZONE.localize(datetime.strptime(' '.join([date, time]), '%d.%m.%Y %H:%M'))
        article_body = soup.find('div', id='article-box').find_all('p')
        article_text = '\n\n'.join([p.text.strip() for p in article_body])

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
                existing_article.text = text
                changed = True
            if changed:
                existing_article.save()
        except self.ARTICLE_MODEL.DoesNotExist:
            article = self.ARTICLE_MODEL(url=url, haaretz_id=haaretz_id, title=title,
                subtitle=subtitle, text=article_text, date=article_date)
            article.save()

            images = soup.find('div', id='article-box').find_all('div', class_='inArticleHoldImage')
            print images
            for image in images:
                img = image.find('img')
                img_url = 'http://www.haaretz.co.il{}'.format(img['src'].split('_gen')[0])
                caption = img.title

                name, image_file = get_file_from_url(img_url)

                article_image, created = self.IMAGE_MODEL.objects.get_or_create(article=article,
                    origin_url=img_url, defaults={'caption': caption})

                if created:
                    article_image.image.save(name, image_file)
                    article_image.save()

    def clean_article_href(self, href):
        href = href.replace('.premium-', '').split('#')[0]
        return super(HaaretzParser, self).clean_article_href(href)
