from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from newsdiff.core.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^haaretz/(?P<id>[\d\.]+)$', HaaretzArticleView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.ENV == 'local':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
