import logging

from newsdiff.celery import app
from newsdiff.core.utils import get_file_from_url

from .models import Document


@app.task()
def import_document(url):
    name, doc = get_file_from_url(url)
    document = Document(url=url)
    document.document.save(name, doc)
    document.save()
