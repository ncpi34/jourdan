from django.db import models
from django_countries.fields import CountryField
from .custom_user import CustomUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    """
    Address
    """
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, primary_key=True, )
    street = models.CharField(_('rue'), max_length=100, null=True)
    apartment = models.CharField(_('appartement'), max_length=100, null=True)
    zip = models.CharField(_('CP'), max_length=10, null=True)
    city = models.CharField(_('ville'), max_length=50, null=True)
    country = CountryField(multiple=False, default='FR')

    @receiver(post_delete, sender=CustomUser)
    def handle_deleted_user(sender, instance, **kwargs):
        if instance:
            try:
                instance.address.delete()
            except ObjectDoesNotExist:
                pass

    class Meta:
        app_label = 'account'

    def __str__(self):
        return self.user.email
