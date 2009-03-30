from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('userprofile.urls')),
    (r'^content/', include('content.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % (settings.MEDIA_URL.lstrip('/')),
         'django.views.static.serve',
                {
                    'document_root': settings.MEDIA_ROOT,
                }),
    )
