from django.db import models
from django_resized import ResizedImageField
from website.functions.helpers import RandomFileName
from website.models import SingletonModel


class DeliveryText(SingletonModel):
    title = models.TextField(default="")
    text = models.TextField(default="")
    picture = ResizedImageField(max_length=10000000, size=[500, 300], upload_to=RandomFileName('img/home'),
                                quality=80, blank=True, null=True)

    class Meta:
        app_label = 'website'
        # ordering = ('nom',)
        verbose_name = 'partie 3 accueil'
        verbose_name_plural = 'partie 3 accueil'

    def __unicode__(self):
        return self.id
