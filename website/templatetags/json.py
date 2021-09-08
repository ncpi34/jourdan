from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.utils.safestring import mark_safe, SafeString
from django import template
import json

register = template.Library()


@register.filter(is_safe=True)
def json(qs):
    return serialize('json', qs, fields=('name', 'rate_VAT', 'price_without_taxes',))
