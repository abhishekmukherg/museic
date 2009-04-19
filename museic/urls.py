from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

import museic.content.settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'base.html'},
        name="home",
        ),
    (r'^ajax/', include('ajax.urls')),
    (r'^accounts/', include('userprofile.urls')),
    (r'^collaborations/', include('content.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % (settings.MEDIA_URL.strip('/')),
         'django.views.static.serve',
                {
                    'document_root': settings.MEDIA_ROOT,
                }),
        (r'^%s/(?P<path>.*)$' % settings.MUSEIC_CONTENT_PREFIX.strip('/'),
         'django.views.static.serve',
                {
                    'document_root': settings.MUSEIC_CONTENT_ROOT,
                }),
    )
