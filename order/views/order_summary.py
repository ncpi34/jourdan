from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from order.models import Order
from django.db.models import Q
import logging
from typing import Union, List

db_logger = logging.getLogger('db')


class OrderSummaryView(LoginRequiredMixin, ListView):
    """
    Order Summary
    """
    template_name = 'order/order_summary.html'
    queryset = Order.objects.all()
    context_object_name = 'histories'

    def get_queryset(self):
        try:
            db_logger.info("order/order_summary.get_queryset")
            # get arg in url
            _user: int = self.request.user.id
            db_logger.info(f"_user => {_user}")

            # filter orders
            history = Order.objects.filter(
                Q(user__id=_user)
            ).exclude(
                Q(status='PendingPayment')
            ).order_by(
                '-date'
            )
            return history
        except Exception as e:
            db_logger.exception(f"erreur order/order_summary => {e}")
