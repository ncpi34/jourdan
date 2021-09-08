from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def to_str(value):
    """converts int to string"""
    return str(value)
