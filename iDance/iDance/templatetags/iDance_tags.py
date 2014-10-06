from django import template
from iDance import utilities

register = template.Library()
from django.template.defaultfilters import floatformat

@register.filter
def percent(value):
    if value is None:
        return None
    return floatformat(value * 100.0, 2) + '%'
    
@register.filter
def rankString(value):
    if value is None:
        return None
    return utilities.rankString(value)