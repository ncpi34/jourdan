from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def custom_input_step(price_type):
    if price_type == "1":
        return str(0.001)
    return str(1)
