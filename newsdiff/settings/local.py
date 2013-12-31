from .base import *

ENV = 'local'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newsdiff',
        'USER': 'newsdiff',
        'PASSWORD': 'newsdiff',
        'HOST': '',
        'PORT': '',
    }
}


MEDIA_ROOT = PROJECT_DIR.child('media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_ALWAYS_EAGER = True  # Makes all celery tasks run synchronously
BROKER_URL = 'redis://localhost:6379/0'
