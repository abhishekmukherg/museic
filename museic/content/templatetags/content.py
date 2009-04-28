from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def tagurl(prefix, tag):
    return reverse(prefix + '_tags', kwargs={'tag': tag.name})
