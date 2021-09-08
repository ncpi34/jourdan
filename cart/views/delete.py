from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from account.views import save_cart_before_logout
from cart.cart import Cart
from website.models import Article
import logging

db_logger = logging.getLogger('db')


class CartRemoveView(View):
    """
    Remove item from cart
    """

    def post(self, request, **kwargs):
        try:
            db_logger.info("DEBUT cart/cart_add")

            cart = Cart(request)  # get cart

            _pk: int = kwargs.get("product_id")  # get arg in url
            db_logger.info(f"_pk => {_pk}")

            product = get_object_or_404(Article, id=_pk)  # get product
            db_logger.info(f"product => {product}")

            cart.remove(product)  # remove article

            if request.user.is_authenticated:
                # save cart to db
                save_cart_before_logout(request)

            db_logger.info("FIN cart/cart_add")
            return redirect("cart:cart_detail")
        except Exception as e:
            db_logger.exception(f"erreur cart/delete => {e}")
