from django.db import models

from website.functions.helpers import RandomFileName
from website.models import SingletonModel


class CGV(SingletonModel):
    file = models.FileField(upload_to=RandomFileName('pdf/'))

    class Meta:
        app_label = 'website'
        # ordering = ('nom',)
        verbose_name = 'fichier CGV'
        verbose_name_plural = 'fichier CGV'
