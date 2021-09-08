import json

from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from account.views import save_cart_before_logout
from cart.cart import Cart
from order.models import Order, OrderItems
from payment.functions import save_order
import logging

db_logger = logging.getLogger('db')


@require_POST
def leave_message(request) -> json:
    """
    Get Price with delivery
    only http post
    Args:
        request: request

    Returns: json

    """
    db_logger.info("DEBUT cart/leave_msg")
    try:
        print('ta madre')
        req: dict = json.loads(request.body)  # get json body
        db_logger.info(f"recuperation json => {req}")
        msg: str = req["data"] # get msg
        db_logger.info(f"recuperation message => {msg}")

        # create order, adding msg
        order, created = Order.objects.get_or_create(
            user=request.user,
            status="PendingPayment"
        )
        db_logger.info("recuperation ou creation commande")
        order.message = msg
        order.save()
        db_logger.info(f"ajout du message a la commande => {msg}")

        db_logger.info("FIN cart/leave_msg")
        return JsonResponse({"msg": "Message pris en compte"}, status=200)
    except Exception as e:
        messages.error(request, "Une erreur est survenue")
        db_logger.exception(f"erreur fin fichier (cart/leave_msg)=> {e}")
        return JsonResponse({"msg": "Erreur"}, status=500)
