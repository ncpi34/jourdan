from django.db import models
from website.models.singleton import SingletonModel


class StripeKey(SingletonModel):
    """
    Keys for Stripe
    """
    public_key = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=200)

    class Meta:
        app_label = 'account'
        verbose_name = "Clés Stripe"

    def __str__(self):
        return self.public_key

    def get_public_key(self):
        return f'{self.public_key}'

