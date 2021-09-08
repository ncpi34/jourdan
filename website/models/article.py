from django.db import models
from django.urls import reverse
from decimal import Decimal
from django_resized import ResizedImageField
from website.functions.helpers import RandomFileName


class Article(models.Model):
    """
    Article
     """
    name = models.CharField(max_length=150, null=True)
    price_with_taxes = models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=3)
    # price by kg ?
    price_type = models.IntegerField(null=True, blank=True)
    article_code = models.CharField(max_length=25, unique=True, null=True)
    description = models.TextField(null=True)
    # slug = models.SlugField(max_length=200, db_index=True, null=True)
    picture = ResizedImageField(max_length=10000000, size=[500, 300], upload_to=RandomFileName('img/product'),
                                quality=80, blank=True, null=True)

    nb_views = models.IntegerField(default=0)

    group = models.ForeignKey('Group',
                              on_delete=models.CASCADE,
                              related_name='article_by_group',
                              null=True)
    family = models.ForeignKey('Family',
                               on_delete=models.CASCADE,
                               related_name='article_by_family',
                               null=True)

    class Meta:
        app_label = 'website'
        ordering = ['article_code']
        verbose_name = 'article'
        # index_together = (('id', 'code_article'), )

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('website:product_detail',
                       args=[self.id])

    def get_price_kg_with_taxes(self):
        print(round(self.price_by_kg * (1 + self.rate_VAT / 100), 2))
        return round(self.price_by_kg * (1 + self.rate_VAT / 100), 2)

    def get_price_with_taxes(self):
        return round(Decimal(self.price_without_taxes * (1 + self.rate_VAT / 100)), 3)

    def get_img(self):
        if self.picture:
            return f'/media/{self.picture}'
        pic = "/media/img/nophoto.jpg"
        return pic

    get_img.short_description = 'Image'
    get_img.allow_tags = True
