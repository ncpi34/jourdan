from django.shortcuts import render
import random
import string

from order.models import OrderItems


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': OrderItems.objects.all()
    }
    return render(request, "website/product/products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid
