from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from museic.content.models import TextContent, AudioContent
import museic.content.forms
import itertools
from os.path import join

def _get_dicts(model, model_name):
    content = {'queryset': model.objects.all()}
    detail = dict(itertools.chain(content.iteritems(),
        {'template_name': join('content', 'content_detail.html')}.iteritems()))
    list = dict(itertools.chain(content.iteritems(),
        {'template_name': join('content', 'content_list.html'),
            'model_name': model_name}.iteritems()))
    return content, detail, list

textcontent_dict, textdetail_dict, textlist_dict = _get_dicts(TextContent,
                                                        "Text Collaborations")

audiocontent_dict, audiodetail_dict, audiolist_dict = _get_dicts(AudioContent,
                                                        "Audio Collaborations")

urlpatterns = patterns('',    
    url(r'^text/by-id/(?P<object_id>\d+)/$',
        'django.views.generic.list_detail.object_detail',
        kwargs=textdetail_dict,
        name="textcontent_details_id"
        ),

    url(r'^text/by-name/(?P<slug>.*)/$',
        'django.views.generic.list_detail.object_detail',
        kwargs=textdetail_dict,
        name="textcontent_details_slug"),
        
    url(r'^text/post/',
        'museic.content.views.create_text_content',
        kwargs={'form_class': museic.content.forms.TextContentForm},
        name="textcontent_create_object"),

    url(r'^text/$',
        'django.views.generic.list_detail.object_list',
        kwargs=textlist_dict,
        name="textcontent_object_list",
        ),

    url(r'^audio/post/$',
        'museic.content.views.create_text_content',
        kwargs={'form_class': museic.content.forms.AudioContentForm},
        name="audiocontent_create_object"),

    url(r'^audio/by-id/(?P<object_id>\d+)/$',
        'django.views.generic.list_detail.object_detail',
        kwargs=audiodetail_dict,
        name="audiocontent_details_id",
        ),
)
