from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
@stringfilter
def url(var):
    return reverse(var)
