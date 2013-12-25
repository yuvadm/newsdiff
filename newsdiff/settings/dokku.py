import dj_database_url

from os import environ
from .base import *

ENV = 'dokku'

DATABASES = {
    'default': dj_database_url.config()
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
