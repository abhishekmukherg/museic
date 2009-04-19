"""
Views for user posted content
"""

import os

from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import get_model_and_form_class
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext

@login_required
def create_text_content(request, model=None, form_class=None):
    """Creates a view based on template_name template and fills in the user"""
    assert model or form_class
    model, form_class = get_model_and_form_class(model, form_class)
    template_name = os.path.join('content', 'textcontent_form.html')
    instance = model(user=request.user)
    if request.method == 'POST':
        form = form_class(request.POST or None,
                          request.FILES or None,
                          instance=instance)
        if form.is_valid():
            new_object = form.save()
            request.user.message_set.create(message=ugettext(
                    "The %(verbose_name)s was created successfully.")
                    % {"verbose_name": model._meta.verbose_name})
            return HttpResponseRedirect(new_object.get_absolute_url())
    else:
        form = form_class(instance=instance)
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label,
                                         model._meta.object_name.lower())
    template = loader.get_template(template_name)
    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))

