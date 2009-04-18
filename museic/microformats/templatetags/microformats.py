from django import template
import django.template.defaultfilters
from django.utils.safestring import mark_safe

register = template.Library()

def microformats_date(var, arg):
    date = django.template.defaultfilters.date(var, r"Y-m-d\TH-i-sO")
    return mark_safe('<abbr class="%s" title="%s">' % (arg, date))
microformats_date.is_safe = True
register.filter(microformats_date)
