from django.db import models
from django.db.models import JSONField


class CartNotFinalized(models.Model):
    user = models.IntegerField()
    data = JSONField()

    def __unicode__(self):
        return self.user
