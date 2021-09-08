from django.db import models
from django.core.exceptions import ValidationError


class Cart(models.Model):
    """
    Cart
    """
    article = models.OneToOneField('Article', on_delete=models.CASCADE, primary_key=True, )

    class Meta:
        app_label = 'website'
        # ordering = ('nom',)
        verbose_name = 'panier'
        verbose_name_plural = 'paniers'

    def __unicode__(self):
        return self.article.pk

    def __str__(self):
        return self.article.name

    def get_article(self):
        return self.article

    def clean(self):
        number = Cart.objects.all().count()
        if number < 3:
            self.save()
        else:
            raise ValidationError(f"Vous ne pouvez pas créer plus de  {number} paniers")
