from django.db import models
from .singleton import SingletonModel


class PaymentCondition(SingletonModel):
    text = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'website'
        verbose_name = "paiement conditions"
        verbose_name_plural = 'paiement conditions'

    def __unicode__(self):
        return self.text

