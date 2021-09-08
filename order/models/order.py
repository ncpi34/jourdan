from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from account.models import Address, CustomUser

STATUS_CHOICES = (
    ('PendingPayment', 'Pending Payment'),
    ('Ordered', 'Ordered'),
    ('Paid', 'Paid'),
    ('Preparation', 'Preparation'),
    ('Send', 'Send'),
    ('Received', 'Received'),
    ('Done', 'Done'),
    ('Canceled', 'Canceled'),
    ('RefundRequest', 'Refund Request'),
    ('RefundGranted', 'Refund Granted'),
)


class Order(models.Model):
    """
    Order
    """
    user = models.ForeignKey(CustomUser,
                             related_name='order_user',
                             on_delete=models.CASCADE,
                             null=True)
    delivery = models.BooleanField(_('livraison'), default=False)
    date = models.DateTimeField(auto_now=True)
    unique_number = models.CharField(max_length=100, null=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    stripe_id = models.CharField(max_length=150, blank=True, null=True)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, null=True)
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', on_delete=models.SET_NULL, null=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'order'
        ordering = ('-date',)
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return 'Commande {}'.format(self.id)

    def get_absolute_url(self):
        return reverse('order:order_detail',
                       args=[self.id])

    @property
    def yearpublished(self):
        return self.date.strftime('%Y')

    @property
    def monthpublished(self):
        return self.date.strftime('%m')

    def get_number_products(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total

    def status_color(self):
        switcher = {
            'PendingPayment': 'warning',
            'Paid': 'success',
            'Preparation': 'warning',
            'Send': 'success',
            'Received': 'success',
            'Done': 'success',
            'Canceled': 'danger',
            'RefundRequest': 'warning',
            'RefundGranted': 'success',
        }
        return switcher.get(self.status, "success")

    def format_status(self):
        switcher = {
            'PendingPayment': 'En attente de paiement',
            'Paid': 'Payé',
            'Ordered': 'Commandé non payé',
            'Preparation': 'En préparation',
            'Send': 'Envoyé',
            'Received': 'Reçu',
            'Done': 'Terminé',
            'Canceled': 'Annulé',
            'RefundRequest': 'Demande de remboursement',
            'RefundGranted': 'Remboursement accordé',
        }
        return switcher.get(self.status, "Statut invalide")

    def get_total_cost(self):
        return round(sum(item.get_cost_with_taxes() for item in self.items.all()), 2)
    get_total_cost.short_description = 'TTC'

    def get_articles(self):
        return [item.get_article() for item in self.items.all()]
