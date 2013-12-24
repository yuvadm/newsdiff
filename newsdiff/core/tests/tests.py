from bs4 import BeautifulSoup
from django.test import TestCase
from unipath import FSPath as Path

from newsdiff.core.parsers.haaretz import HaaretzParser

class HaaretzParsingTestCase(TestCase):

    CONTENT_DIR = Path(__file__).absolute().parent.child('content')

    def setUp(self):
        self.parser = HaaretzParser()

    def _get_content(self, filename):
        with open(self.CONTENT_DIR.child(filename), 'r') as f:
            return f.read()

    def test_parse_homepage(self):
        soup = BeautifulSoup(self._get_content('haaretz.html'))
        articles = self.parser.parse_homepage(soup)
        self.assertTrue(articles)
