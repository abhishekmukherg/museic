from django import template
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.filter
def module_name(var):
    return var.meta.verbose_name
