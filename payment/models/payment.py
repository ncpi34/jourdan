from django.db import models
from account.models import CustomUser


class Payment(models.Model):
    """
    Payment
    """
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'payment'

    def __unicode__(self):
        return self.pk
