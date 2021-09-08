from django.db import models
from website.models import SingletonModel


class HomeText(SingletonModel):
    line = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'website'
        # ordering = ('nom',)
        verbose_name = 'texte horaires ouvertures'
        verbose_name_plural = 'texte horaires ouvertures'

    def __str__(self):
        return self.line
