from django.db import models

from account.models.custom_user import CustomUser


class FavoritesClient(models.Model):
    """
    Favorites
    """
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='user_favorite',
                             )
    article = models.ForeignKey('Article',
                                on_delete=models.CASCADE,
                                related_name='article_favorite',
                                )
    quantity = models.IntegerField(default=0)

    class Meta:
        app_label = 'website'
        # ordering = ('nom',)
        verbose_name = 'favoris'
        verbose_name_plural = 'favoris'

    def __unicode__(self):
        return self.user.id

    def __str__(self):
        return self.article.name

    def format_data_in_dict(self):
        return {'pk': self.article.pk, 'quantity': self.quantity }

    # def clean(self):
    #     numFavorites = FavorisClient.objects.all().count()
    #     if numFavorites > 19:
    #         raise ValidationError("Vous ne pouvez pas créer plus de  {} favoris".format(numFavorites))
