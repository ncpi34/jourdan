from django.db import models
from .singleton import SingletonModel


class HarborCeilings(SingletonModel):

    drive = models.IntegerField(default=50, verbose_name="drive")
    delivery = models.IntegerField(default=100, verbose_name="livraison")


    class Meta:
        app_label = 'website'
        verbose_name = "Plafonds drive & livraison"
        verbose_name_plural = 'Plafonds drive & livraison'

    def __str__(self):
        return f"{self.pk}"
