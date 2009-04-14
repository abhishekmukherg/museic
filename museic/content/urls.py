from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
import museic.content.models
from os.path import join

info_dict = {'queryset': museic.content.models.TextContent.objects.all(),
                'template_name': join('content', 'content_detail.html')}


urlpatterns = patterns('',    
    url(r'^text/by-id/(?P<object_id>\d+)/$',
        'django.views.generic.list_detail.object_detail',
        kwargs=info_dict,
        name="textcontent_details_id"
        ),

    url(r'^text/by-name/(?P<slug>.*)/$',
        'django.views.generic.list_detail.object_detail',
        kwargs=info_dict,
        name="textcontent_details_slug"),
        
    url(r'^text/post/',
        'django.views.generic.create_update.create_object',
        {'model': museic.content.models.TextContent,
            'login_required': True},
        name="textcontent_create_object"),
)
