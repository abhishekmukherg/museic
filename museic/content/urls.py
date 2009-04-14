from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import museic.content.models
import itertools
from os.path import join

textcontent_dict = {'queryset': museic.content.models.TextContent.objects.all()}

detail_dict = dict(itertools.chain(textcontent_dict.iteritems(),
                {'template_name': join('content', 'content_detail.html')}.iteritems()))

list_dict = dict(itertools.chain(textcontent_dict.iteritems(),
                {'template_name': join('content', 'content_list.html')}.iteritems()),
                extra_context={'model_name': _('Text Collaborations')})


urlpatterns = patterns('',    
    url(r'^text/by-id/(?P<object_id>\d+)/$',
        'django.views.generic.list_detail.object_detail',
        kwargs=detail_dict,
        name="textcontent_details_id"
        ),

    url(r'^text/by-name/(?P<slug>.*)/$',
        'django.views.generic.list_detail.object_detail',
        kwargs=detail_dict,
        name="textcontent_details_slug"),
        
    url(r'^text/post/',
        'django.views.generic.create_update.create_object',
        {'model': museic.content.models.TextContent,
            'login_required': True},
        name="textcontent_create_object"),

    url(r'^text/$',
        'django.views.generic.list_detail.object_list',
        kwargs=list_dict,
        name="textcontent_object_list",
        ),
)
