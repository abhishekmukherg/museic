from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
def rate_percentage(var, outof):
    return (var * 100) // int(outof)

@register.filter
@stringfilter
def rate_url(prefix):
    return reverse(prefix+'content_vote')
