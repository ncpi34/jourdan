import json

from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from account.models import Address
from account.views import save_cart_before_logout
from cart.cart import Cart
from order.models import Order, OrderItems
from payment.functions import save_order
import logging

db_logger = logging.getLogger('db')


def join_total_TTC(order):
    total = str(order.get_total_cost()).split('.')
    return "".join(total)


@require_POST
def get_price_with_delivery(request) -> json:
    """
    Get Price with delivery
    only http post
    Args:
        request: request

    Returns: json

    """
    db_logger.info("DEBUT cart/get_total_with_delivery")
    try:
        req = json.loads(request.body)  # get json body
        db_logger.info("recuperation json")
        result = True  # default =delivery
        db_logger.info("livraison par default")

        if req['data'] == "click_and_collect":
            db_logger.info("changement livraison: click & collect")
            result = False  # changing delivery to click & collect

        # get user address
        address = Address.objects.filter(user=request.user)
        if not address.exists():
            db_logger.error(f"no address found {address}")
            return JsonResponse({"msg": "Fournissez une adresse dans votre espace"}, status=500)

        # create order, adding delivery opt, and unique number
        order, created = Order.objects.update_or_create(
            user=request.user,
            status="PendingPayment",
            defaults={
                'shipping_address': address.first(),
                'billing_address': address.first(),
            }

        )
        db_logger.info("recuperation ou creation commande")

        # change values order
        order.delivery = result
        order.unique_number = order.pk
        order.save()
        db_logger.info("modification livraison et numero unique")

        db_logger.info("FIN cart/get_total_with_delivery")
        return JsonResponse({
            "msg": "success",
        }, status=200)
    except Exception as e:
        messages.error(request, "Une erreur est survenue")
        db_logger.exception(f"erreur fin fichier (cart/get_total_with_delivery)=> {e}")
        return JsonResponse({"msg": "error"}, status=500)
