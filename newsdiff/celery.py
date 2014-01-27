from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings
from raven import Client
from raven.contrib.celery import register_signal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsdiff.settings')

app = Celery('newsdiff')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

raven_client = Client(os.environ.get('SENTRY_DSN'))
register_signal(raven_client)
