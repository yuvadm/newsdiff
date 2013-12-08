import urllib2

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urlparse import urlparse

def get_image_from_url(url):
    tmp = NamedTemporaryFile(delete=True)
    u = urllib2.urlopen(url)
    tmp.write(u.read())
    tmp.flush()
    name = urlparse(u.geturl()).path.split('/')[-1]
    return name, File(tmp)
