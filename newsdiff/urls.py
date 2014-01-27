from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse

from newsdiff.core.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^haaretz$', HaaretzListView.as_view(), name='haaretz_recent'),
    url(r'^haaretz/(?P<id>[\d\.]+)$', HaaretzArticleView.as_view(), name='haaretz_article'),
    url(r'^ynet$', YnetListView.as_view(), name='ynet_recent'),
    url(r'^ynet/(?P<id>[\d]+)$', YnetArticleView.as_view(), name='ynet_article'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt', lambda x: HttpResponse('User-agent: *\nDisallow: /', mimetype='text/plain'))
)

if settings.ENV == 'local':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
