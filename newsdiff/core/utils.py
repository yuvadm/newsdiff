import logging
import requests

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.parse import urlparse


def get_file_from_url(url):
    tmp = NamedTemporaryFile(delete=True)
    req = requests.get(url)
    if not req.ok:
        logging.error('Failed to import image from {}'.format(url))
        return None
    tmp.write(req.content)
    tmp.flush()
    name = urlparse(req.url).path.split('/')[-1]
    return name, File(tmp)
