import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from account.models import Address
from account.views import save_cart_before_logout
from cart.cart import Cart
from cart.forms import CartUpdateProductForm
from cart.order_process import order_process
from website.models import Article
import logging

db_logger = logging.getLogger('db')


@require_POST
def cart_update(request):
    """
    Update cart
    """
    db_logger.info("DEBUT cart/update")
    try:
        data = json.loads(request.body)
        db_logger.info(f"data {data}")

        # get cart
        cart = Cart(request)
        db_logger.info(f"cart => {cart}")

        # get product
        qs_product: [Article] = Article.objects.filter(id=int(data['article_id']))
        db_logger.info(f"qs_product => {qs_product}")

        cart.add(product=qs_product[0],
                 quantity=str(data['quantity']),
                 )
        if request.user.is_authenticated:
            # save cart to db
            save_cart_before_logout(request)

        db_logger.info("product qty updated")
        return JsonResponse({"total": cart.get_total_price(), "cartLength": cart.__len__()}, status=200)

    except Exception as e:
        db_logger.exception(f"erreur cart/cart_update => {e}")
        return JsonResponse({"msg": "Erreur"}, status=500)
