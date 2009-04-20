from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.html import escape
from django.contrib import comments
from django.contrib.comments import signals
from django.utils.translation import ugettext as _
from museic.microformats.templatetags.microformats import microformats_date
from django.contrib.humanize.templatetags.humanize import naturalday
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.shortcuts import get_object_or_404
import simplejson
import museic.content.views

def json_error(error):
    status = simplejson.dumps({'status': 'debug', 'error': error})
    return http.HttpResponseServerError(status, mimetype='application/json')

def ajax_comment_post(request):
    """
    Post a comment.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.username
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return json_error(_("Missing content_type or object_pk field."))
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
    except TypeError:
        return json_error(_("Invalid content_type value: %r") % escape(ctype))
    except AttributeError:
        return json_error(
            _("The given content-type %r does not resolve to a valid model.")
            % escape(ctype))
    except ObjectDoesNotExist:
        return json_error(
            _("No object matching content-type %r and object PK %r exists.")
            % (escape(ctype), escape(object_pk)))

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = comments.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return json_error(
            _("The comment form failed security verification: %s")
            % escape(str(form.security_errors())))

    # If there are errors or if we requested a preview show the comment
    if form.errors or preview:
        error = ""
        for e in form.errors:
            error += _("Error in the %s field: %s") % (e, form.errors[e])
        status = simplejson.dumps({'status': 'error', 'error': error})
        return http.HttpResponse(status, mimetype='application/json')

    # Otherwise create the comment
    comment = form.get_comment_object()
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
    if request.user.is_authenticated():
        comment.user = request.user

    # Signal that the comment is about to be saved
    responses = signals.comment_will_be_posted.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )

    for (receiver, response) in responses:
        if response == False:
            return json_error(
                _("comment_will_be_posted receiver %r killed the comment")
                    % receiver.__name__)

    # Save the comment and signal that it was saved
    comment.save()
    signals.comment_was_posted.send(
        sender  = comment.__class__,
        comment = comment,
        request = request
    )
    status = simplejson.dumps({'status': 'success',
                               'comment': unicode(comment.comment),
                               'url': comment.user.get_absolute_url(),
                               'name': comment.user_name,
                               'uday': microformats_date(comment.submit_date,
                                                        'submit_date'),
                               'day' : naturalday(comment.submit_date),
                               })
    return http.HttpResponse(status, mimetype='application/json')

def ajax_vote(request, model):
    try:
        museic.content.views.vote(request, model)
    except Http404:
        return json_error("Could not register vote")
    except TemplateDoesNotExist:
        pass
    instance = get_object_or_404(model, pk=int(request.REQUEST['id']))
    status = simplejson.dumps({'status': 'success',
                'votes': instance.rating.votes,
                'score': instance.rating.score,
                })
    return http.HttpResponse(status, mimetype='spplication/json')


