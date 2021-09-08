from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from order.models import Order
import logging

db_logger = logging.getLogger('db')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Order Detail
    """
    template_name = 'order/order_detail.html'
    queryset = Order.objects.all()

    def get_object(self, **kwargs):
        db_logger.info("in order/order_detail.get_context_data")
        # get id in url
        _id: int = self.kwargs.get('pk')
        db_logger.info(f"_id => {_id}")
        return get_object_or_404(Order, pk=_id)

    def get_context_data(self, **kwargs):
        db_logger.info("in order/order_detail.get_context_data")
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        db_logger.info("after context")
        return context
