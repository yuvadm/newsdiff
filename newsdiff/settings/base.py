from datetime import timedelta
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Yuval Adam', 'yuv.adm@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = []

TIME_ZONE = 'Asia/Jerusalem'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    str(PROJECT_DIR / 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'N0_oNe_U53s_th1S_f#$^ing_k3y_:)'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'newsdiff.urls'

WSGI_APPLICATION = 'newsdiff.wsgi.application'

TEMPLATE_DIRS = (
    str(PROJECT_DIR / 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'gunicorn',
    'storages',
    'celery',
    'reversion',
    'sorl.thumbnail',

    'newsdiff.core',
    'newsdiff.docs',
    'newsdiff.rain'
)

AUTH_USER_MODEL = 'core.NewsDiffUser'

SITE_ID = 1

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERYBEAT_SCHEDULE = {
    'rain': {
        'task': 'newsdiff.rain.tasks.import_rain_radar_image',
        'schedule': timedelta(minutes=10)
    },
    'haaretz_homepage': {
        'task': 'newsdiff.core.tasks.process_haaretz_homepage',
        'schedule': timedelta(minutes=15)
    },
    'ynet_homepage': {
        'task': 'newsdiff.core.tasks.process_ynet_homepage',
        'schedule': timedelta(minutes=15)
    }
}
