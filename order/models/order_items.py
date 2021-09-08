from django.db import models
from order.models import Order


class OrderItems(models.Model):
    """
    Items
    """
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    article_code = models.CharField(max_length=25, null=True)
    name = models.CharField(max_length=150, null=True)
    price_with_taxes = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2)
    price_type = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'order'
        ordering = ('name',)
        verbose_name = 'Produits Commandés'
        verbose_name_plural = 'Produits Commandés'

    def __str__(self):
        return self.name

    def get_unit_cost_with_taxes(self):
        return self.price_with_taxes

    def get_cost_with_taxes(self):
        return round(float(self.price_with_taxes) * self.quantity, 2)
    get_cost_with_taxes.short_description = 'TTC'

    def get_article(self):
        return self
