from rest_framework import serializers
from order.models import Order, OrderItems
from website.models import Novelties


class NoveltiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Novelties
        fields = []

    def to_representation(self, instance):
        # response = super().to_representation(instance)
        response = {
            "id": instance.pk,
            "article_id": instance.article.id,
            "name": instance.article.name,
            "barcode": instance.article.barcode,
            "article_code": instance.article.article_code,
            "price_without_taxes": instance.article.price_without_taxes,
            "stock": instance.article.stock,
        }
        return response
