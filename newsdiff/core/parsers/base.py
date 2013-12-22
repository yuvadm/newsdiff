import re
import requests

from pytz import timezone


class HtmlSoupParser(object):

    HTTP_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    TIMEZONE = timezone('Asia/Jerusalem')

    def get_page(self, url):
        req = requests.get(url, headers=HTTP_HEADERS)
        if req.ok:
            return BeautifulSoup(req.text, 'lxml')

    def get_homepage(self):
        return get_page(self.HOMEPAGE_URL)

    def parse_article(self, url):
        raise NotImplementedError

    def clean_article_href(self, href):
        return href
