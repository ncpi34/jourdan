from django.db import models
from website.models import SingletonModel
from django.utils.translation import gettext_lazy as _


class Stripe(SingletonModel):
    public_key = models.CharField(_('clé publique'), max_length=255, blank=True, null=True)
    private_key = models.CharField(_('clé privée'), max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'payment'
        verbose_name = "stripe"
        verbose_name_plural = 'stripe'

