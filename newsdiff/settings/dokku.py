import dj_database_url

from os import environ
from .base import *

ENV = 'dokku'

ALLOWED_HOSTS = (
    environ.get('PUBLIC_HOSTNAME'),
)

DATABASES = {
    'default': dj_database_url.config()
}

STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME')
STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
