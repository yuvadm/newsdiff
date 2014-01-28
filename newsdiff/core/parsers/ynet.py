import re
import requests
import reversion

from bs4 import BeautifulSoup
from datetime import datetime
from django.db import transaction

from .base import HtmlSoupParser
from ..models import YnetArticle, YnetImage
from ..utils import get_file_from_url


class YnetParser(HtmlSoupParser):

    BASE_URL = 'http://www.ynet.co.il'
    HOMEPAGE_URL = BASE_URL + '/home/0,7340,L-2,00.html'
    ARTICLE_HREF_PATTERN = re.compile(r'''^(http:\/\/www\.ynet\.co\.il)?/articles/0,7340,L-\d\d\d\d\d\d\d,00\.html$''')
    ARTICLE_ID_PATTERN = re.compile(r'\d\d\d\d\d\d\d')
    ARTICLE_MODEL = YnetArticle
    IMAGE_MODEL = YnetImage

    def article_id_to_url(self, article_id):
        return self.HOMEPAGE_URL.replace('L-2', 'L-{}'.format(article_id))

    def parse_article(self, url, soup):
        ynet_id = re.findall(self.ARTICLE_ID_PATTERN, url)[0]
        title = soup.find('div', class_='art_header_title').text.strip().encode('iso-8859-1')
        try:
            subtitle = soup.find('div', class_='art_header_sub_title').text.strip().encode('iso-8859-1')
        except:
            subtitle = ''
        author_bar = soup.find('span', class_='art_header_footer_author')
        author = author_bar.find('a').text.strip().encode('iso-8859-1')
        date = re.findall(r'\d\d.\d\d.\d\d', author_bar.text)[0]
        time = re.findall(r'\d\d:\d\d', author_bar.text)[0]
        article_date = self.TIMEZONE.localize(datetime.strptime(' '.join([date, time]), '%d.%m.%y %H:%M'))
        article_body = soup.find('div', class_='art_body').find_all('p')
        try:
            article_text = '\n'.join([p.text.strip().encode('iso-8859-1') for p in article_body if p.text])
        except:
            article_text = '\n'.join([p.text.strip() for p in article_body if p.text])

        with transaction.atomic(), reversion.create_revision():
            try:
                existing_article = self.ARTICLE_MODEL.objects.get(ynet_id=ynet_id)
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
                article = self.ARTICLE_MODEL(url=url, ynet_id=ynet_id, title=title,
                    subtitle=subtitle, author=author, text=article_text, date=article_date)
                article.save()
