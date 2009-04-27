from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

import museic.settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'base.html'},
        name="home",
        ),
    (r'^ajax/', include('museic.ajax.urls')),
    (r'^accounts/', include('userprofile.urls')),
    (r'^collaborations/', include('museic.content.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^notifications/', include('notification.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % (settings.MEDIA_URL.replace(
            settings.SITE_PREFIX, "", 1).strip('/')),
         'django.views.static.serve',
                {
                    'document_root': settings.MEDIA_ROOT,
                }),
        (r'^%s/(?P<path>.*)$' % settings.MUSEIC_CONTENT_PREFIX.replace(
            settings.SITE_PREFIX, "", 1).strip('/'),
         'django.views.static.serve',
                {
                    'document_root': settings.MUSEIC_CONTENT_ROOT,
                }),
    )
