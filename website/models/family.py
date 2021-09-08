from django.db import models
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models import Count
from website.models import Article


class Family(models.Model):
    """
    Family
    """
    name = models.CharField(max_length=200)
    group = models.ForeignKey('Group',
                              null=True,
                              on_delete=models.CASCADE,
                              related_name='families_by_group')
    ref = models.CharField(max_length=50, unique=True, null=True)

    class Meta:
        app_label = 'website'
        ordering = ('name',)
        verbose_name = 'family'
        verbose_name_plural = 'families'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('website:products_by_family',
                       args=[self.name])

    @receiver(post_delete, sender=Article)
    def handle_deleted_article_family(sender, instance, **kwargs):
        articles_by_fam = Family.objects.all().annotate(nbre=Count('article_by_family'))
        for key, value in enumerate(articles_by_fam):
            if value.nbre == 0:
                articles_by_fam[key].delete()

