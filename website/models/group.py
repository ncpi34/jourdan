from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver
from website.models import Article


class Group(models.Model):
    """
    Group
    """
    name = models.CharField(max_length=200)

    class Meta:
        app_label = 'website'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('website:products_by_group',
                       args=[self.name])

    # @receiver(post_delete, sender=Article)
    # def handle_deleted_article_group(sender, instance, **kwargs):
    #     articles_by_gr = Group.objects.all().annotate(nbre=Count('article_by_group'))
    #     for key, value in enumerate(articles_by_gr):
    #         if value.nbre == 0:
    #             articles_by_gr[key].delete()
