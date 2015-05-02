import dj_database_url
from urllib.parse import urlparse

from os import environ
from .base import *

ENV = 'flynn'

ALLOWED_HOSTS = (
    environ.get('PUBLIC_HOSTNAME'),
)

DATABASES = {
    'default': dj_database_url.config()
}

BROKER_URL = REDIS_URL = environ.get('REDIS_URL')
redis_url = urlparse(REDIS_URL)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{}:{}'.format(redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

SECRET_KEY = environ.get('SECRET_KEY')

STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = False
AWS_IS_GZIPPED = True
AWS_S3_SECURE_URLS = False
AWS_HEADERS = {
    # 'Cache-Control': 'public, max-age=86400',
}

RAVEN_CONFIG = {
    'dsn': environ.get('SENTRY_DSN'),
}

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)
