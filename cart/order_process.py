from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from account.views import save_cart_before_logout
from cart.cart import Cart
from cart.forms import CartUpdateProductForm
from order.models import OrderItems, Order
from payment.functions import save_order
from website.models import Article
import logging

db_logger = logging.getLogger('db')


def order_process(request):
    # get order then change date & status(ordered)
    order: [Order] = Order.objects.update_or_create(
        user=request.user,
        status="PendingPayment",
    )
    db_logger.info(f"commande trouvée: {order}")

    # delete items related to the order
    items = OrderItems.objects.filter(order=order[0]).delete()
    db_logger.info(f"suppression des produits lies a la commande => {items}")

    # saving cart not finalized
    # save_cart_before_logout(request)
    db_logger.info("sauvegarde dans la table commande finalisee")

    # retrieve cart session
    cart = Cart(request)
    db_logger.info("recuperation session panier")

    # saving cart in order table with items
    save_order(cart, order[0], request.user)
    db_logger.info("ajout des produits a la commande")

    return order[0]
