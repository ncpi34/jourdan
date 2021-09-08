import json
from django.http import JsonResponse
from django.views.generic import ListView
from website.models import PaymentCondition
from typing import Union, List
import logging

db_logger = logging.getLogger('db')


class PaymentConditionViews(ListView):
    """
    Payment Condition View
    for modal
    """

    def get_queryset(self):
        db_logger.info("DEBUT website/payment_condition")
        # qs filter
        queryset = PaymentCondition.objects.all()
        db_logger.info("qs ok")
        # check if qs is empty or not
        if queryset.exists():
            db_logger.info("qs null")
            return queryset[0].text
        db_logger.info("qs non null")
        return "En attente de conditions"

    def get(self, request, *args, **kwargs):
        try:
            # call method
            queryset = self.get_queryset()
            # data to json
            data = json.dumps(queryset)
            db_logger.info("FIN website/payment_condition")
            return JsonResponse(data, status=200, safe=False)
        except Exception as e:
            db_logger.exception(f"erreur (website/payment_condition)=> {e}")
