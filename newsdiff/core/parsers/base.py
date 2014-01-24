import re
import requests

from bs4 import BeautifulSoup
from pytz import timezone


class HtmlSoupParser(object):

    HTTP_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    TIMEZONE = timezone('Asia/Jerusalem')

    def get_page(self, url):
        req = requests.get(url, headers=self.HTTP_HEADERS)
        return BeautifulSoup(req.text, 'lxml')

    def process_homepage(self):
        soup = self.get_page(self.HOMEPAGE_URL)
        articles = self.parse_homepage(soup)
        for article_url in articles:
            self.process_article(article_url)

    def process_article(self, url):
        soup = self.get_page(url)
        self.parse_article(url, soup)

    def parse_homepage(soup):
        raise NotImplementedError

    def parse_article(self, url):
        raise NotImplementedError

    def clean_article_href(self, href):
        if not href.startswith('http'):
            href = '{}{}'.format(self.BASE_URL, href)
        return href
