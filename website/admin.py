from django.contrib import admin
from django.contrib.auth.models import Group
from website.models import Article, Novelties, HomeText, \
    PaymentCondition, HarborCeilings, Cart, CGV, DeliveryText, GroceryText, CartText

"""Register part"""
admin.site.register(HomeText)
admin.site.register(HarborCeilings)
admin.site.register(Cart)
admin.site.register(CGV)
admin.site.register(DeliveryText)
admin.site.register(GroceryText)
admin.site.register(CartText)


"""Unregister part"""
admin.site.unregister(Group)

""" Site visual """
admin.site.site_header = 'Administration Ats Cash'
