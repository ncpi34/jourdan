import os
from django.urls import reverse_lazy

"""
Custom variables
"""
CART_SESSION_ID = 'cart'  # during 15 days
LOGIN_URL = reverse_lazy("account:login")
SITE_ID = 1
PRODUCT_DOES_NOT_EXISTS_ANYMORE = False
TOO_MUCH_ADDRESSES = False
TOO_MUCH_ADDRESSES_MSG = ''
CT_USER_SESS = {}
CURRENT_SITE = os.getenv("CURRENT_SITE")
DELIVERY_MAIL = os.getenv("DELIVERY_MAIL")
ACCOUNT_MAIL = os.getenv("ACCOUNT_MAIL")