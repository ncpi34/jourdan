from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from order.models import Order, OrderItems
from website.models import Article


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ["article_code", ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['article'] = {
                "article_code": instance.article_code,
                "name": instance.name,
                "price_with_taxes": instance.price_with_taxes,
                "quantity": instance.quantity,
                "price_type": instance.price_type,
            }

        return response


class OrderSerializer(serializers.ModelSerializer):
    items = ItemsSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Order
        ordering = ['date']
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = {
            "email": instance.user.email,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
        }
        response['shipping_address'] = {
            "street": instance.user.address.street,
            "apartment": instance.user.address.apartment,
            "zip": instance.user.address.zip,
            "city": instance.user.address.city,
        }
        response['billing_address'] = {
            "street": instance.user.address.street,
            "apartment": instance.user.address.apartment,
            "zip": instance.user.address.zip,
            "city": instance.user.address.city,
        }
        return response

