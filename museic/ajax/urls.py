from django.conf.urls.defaults import *
import museic.content.models

urlpatterns = patterns('museic.ajax.views',
        url(r'^comment/post/$',
            view='ajax_comment_post',
            name='ajax_comment_post',
            ),
        url(r'^text/rate/$',
            'ajax_vote',
            kwargs={'model': museic.content.models.TextContent},
            ),
        url(r'^audio/rate/$',
            'ajax_vote',
            kwargs={'model': museic.content.models.AudioContent},
            ),
)
