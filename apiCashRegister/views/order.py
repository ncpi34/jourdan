import datetime

from django.db.models import Q
from django.utils import timezone

from apiCashRegister.serializers import OrderSerializer
from order.models import Order, OrderItems
from rest_framework.viewsets import ModelViewSet
from apiCashRegister.functions import IsSuperUser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.conf import settings
from django.utils.timezone import make_aware


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsSuperUser,)
    lookup_field = 'pk'

    def get_queryset(self):
        s_date: str = self.request.query_params.get('date', None)

        if s_date is not None:
            date_obj = datetime.datetime(
                int(s_date[0:4]),
                int(s_date[4:6]),
                int(s_date[6:8]),
                int(s_date[8:10]),
                int(s_date[10:12]),
            )

            # to handle warning
            date_obj.tzinfo  # None
            settings.TIME_ZONE  # 'UTC'
            aware_datetime = make_aware(date_obj)
            aware_datetime.tzinfo
            return self.queryset.filter(Q(date__gt=aware_datetime)).exclude(
                Q(status="PendingPayment") | Q(status="Ordered")
            )

        return self.queryset.exclude(Q(status="PendingPayment") | Q(status="Ordered"))
