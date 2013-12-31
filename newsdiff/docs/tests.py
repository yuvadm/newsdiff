from django.test import TestCase

from .models import Document
from .tasks import import_document


class DocumentTestCase(TestCase):
    def setUp(self):
        pass

    def test_import_document(self):
        import_document('http://www.google.com/webmasters/docs/search-engine-optimization-starter-guide.pdf')
        document = Document.objects.all()[0]
        self.assertTrue(document.created)
        self.assertTrue(document.document.url)
