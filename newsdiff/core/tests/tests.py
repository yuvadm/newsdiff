from bs4 import BeautifulSoup
from django.test import TestCase
from unipath import FSPath as Path

from newsdiff.core.parsers.haaretz import HaaretzParser
from ..models import HaaretzArticle, HaaretzImage

class HaaretzParsingTestCase(TestCase):

    CONTENT_DIR = Path(__file__).absolute().parent.child('content')

    def setUp(self):
        self.parser = HaaretzParser()

    def _get_content(self, filename):
        with open(self.CONTENT_DIR.child(filename), 'r') as f:
            return f.read()

    def _get_soup(self, filename):
        return BeautifulSoup(self._get_content(filename), 'lxml')

    def test_parse_homepage(self):
        soup = self._get_soup('homepage.html')
        articles = self.parser.parse_homepage(soup)
        self.assertEqual(len(articles), 67)

    def test_parse_article(self):
        article_id = '1.2198200'
        soup = self._get_soup('{}.html'.format(article_id))
        self.parser.parse_article(article_id, soup)
        article = HaaretzArticle.objects.get(haaretz_id=article_id)
        self.assertEqual(article.url, 'http://www.haaretz.co.il/{}'.format(article_id))
        images = article.images
        self.assertEqual(images.count(), 2)
