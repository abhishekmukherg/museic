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
            'extra_context': {'model_name': model_name}}.iteritems()))
    return content, detail, list

def _get_url_patterns(prefix, model_name, model, form_class):
    main_dict, detail_dict, list_dict = _get_dicts(model, model_name)
    if 'extra_context' not in detail_dict:
        detail_dict['extra_context'] = {}
    detail_dict['extra_context']['prefix'] = prefix
    return patterns('',
        url(r'^%s/by-id/(?P<object_id>\d+)/$' % prefix,
            'django.views.generic.list_detail.object_detail',
            kwargs=detail_dict,
            name="%scontent_details_id" % prefix,
            ),

        url(r'^%s/by-name/(?P<slug>.*)/$' % prefix,
            'django.views.generic.list_detail.object_detail',
            kwargs=detail_dict,
            name="%scontent_details_slug" % prefix,
            ),
            
        url(r'^post/%s/$' % prefix,
            'museic.content.views.create_text_content',
            kwargs={'form_class': form_class},
            name="%scontent_create_object" % prefix,
            ),

        url(r'^%s/$' % prefix,
            'django.views.generic.list_detail.object_list',
            kwargs=list_dict,
            name="%scontent_object_list" % prefix,
            ),
        url(r'^%s/rate/$' % prefix,
            'museic.content.views.vote',
            kwargs={'model': model},
            name="%scontent_vote" % prefix),
        )

urlpatterns = _get_url_patterns('text',
                                'Text Collaborations',
                                TextContent,
                                museic.content.forms.TextContentForm,
                                )

urlpatterns += _get_url_patterns('audio',
                                'Audio Collaborations',
                                AudioContent,
                                museic.content.forms.AudioContentForm,
                                )
urlpatterns += patterns('django.views.generic.simple',
        url(r'^$',
            'direct_to_template',
            {'template': 'content/collab_landing.html',
                'extra_context': {
                    'text_title': 'Create Text Collaboration',
                    'audio_title': 'Create Audio Collaboration',
                    },
                },
            name='content_collab_landing',
            ),

        url(r'^post/$',
            'direct_to_template',
            {'template': 'content/post_landing.html',
                'extra_context': {
                    'text_title': 'Text Collaborations',
                    'audio_title': 'Audio Collaborations',
                    },
                },
            name='content_post_landing',
            )
        )
