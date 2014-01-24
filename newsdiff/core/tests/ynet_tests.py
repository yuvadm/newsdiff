from bs4 import BeautifulSoup
from django.test import TestCase
from unipath import FSPath as Path

from newsdiff.core.parsers.ynet import YnetParser
from ..models import YnetArticle, YnetImage

class YnetParsingTestCase(TestCase):

    CONTENT_DIR = Path(__file__).absolute().parent.child('content')

    def setUp(self):
        self.parser = YnetParser()

    def _get_content(self, filename):
        with open(self.CONTENT_DIR.child(filename), 'r') as f:
            return f.read()

    def _get_soup(self, filename):
        return BeautifulSoup(self._get_content(filename), 'lxml')

    def test_parse_homepage(self):
        soup = self._get_soup('0,7340,L-2,00.html')
        articles = self.parser.parse_homepage(soup)
        self.assertEqual(len(articles), 49)

    def test_parse_article(self):
        article_id = '4480544'
        article_url = self.parser.article_id_to_url(article_id)
        soup = self._get_soup('{}.html'.format(article_id))
        self.parser.parse_article(article_url, soup)
        article = YnetArticle.objects.get(ynet_id=article_id)
        self.assertEqual(article.url, article_url)
        images = article.images
        self.assertEqual(images.count(), 0)