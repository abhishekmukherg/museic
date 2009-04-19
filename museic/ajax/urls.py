from django.conf.urls.defaults import *

urlpatterns = patterns('museic.ajax.views',
        url(r'^comment/post/$',
            view='ajax_comment_post',
            name='ajax_comment_post',
            ),
        )
