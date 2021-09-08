from django.db import models
from django.core.exceptions import ValidationError


class Novelties(models.Model):
    """
    Novelties
    """
    article = models.OneToOneField('Article', on_delete=models.CASCADE, primary_key=True, )

    class Meta:
        app_label = 'website'
        # ordering = ('nom',)
        verbose_name = 'nouveauté'
        verbose_name_plural = 'nouveautés'

    def __unicode__(self):
        return self.article.pk

    def __str__(self):
        return self.article.name

    def clean(self):
        number = Novelties.objects.all().count()
        if number < 22:
            self.save()
        else:
            raise ValidationError("Vous ne pouvez pas créer plus de  {} nouveautés".format(number))
