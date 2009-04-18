"""
Views for user posted content
"""

import os

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext
from museic.content.forms import TextContentForm
from museic.content.models import TextContent

@login_required
def create_text_content(request):
    """Creates a view based on template_name template and fills in the user"""
    template_name = os.path.join('content', 'textcontent_form.html')
    instance = TextContent(user=request.user)
    if request.method == 'POST':
        form = TextContentForm(request.POST or None,
                               request.FILES or None,
                               instance=instance)
        if form.is_valid():
            new_object = form.save()
            request.user.message_set.create(message=ugettext(
                    "The %(verbose_name)s was created successfully.")
                    % {"verbose_name": TextContent._meta.verbose_name})
            return HttpResponseRedirect(new_object.get_absolute_url())
    else:
        form = TextContentForm(instance=instance)
    if not template_name:
        template_name = "%s/%s_form.html" % (TextContent._meta.app_label,
                                         TextContent._meta.object_name.lower())
    template = loader.get_template(template_name)
    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))

