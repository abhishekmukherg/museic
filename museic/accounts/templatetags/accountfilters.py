from django import template
from django.template.defaultfilters import stringfilter
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
@stringfilter
def notlogout(value):
    if reverse('logout') == value:
        return reverse('home')
    else:
        return value
