import json

from django.views.decorators.http import require_POST

from account.views import save_cart_before_logout
from cart.cart import Cart
from website.models import Article
import logging
from django.http import JsonResponse

db_logger = logging.getLogger('db')


@require_POST
def cart_add(request, product_id):
    """
    Add product to cart
    """

    db_logger.info("DEBUT cart/cart_add")
    data: dict = json.loads(request.body)  # get json body

    # get cart
    cart: Cart = Cart(request)
    db_logger.info(f"cart => {cart}")

    # get article
    qs_product: [Article] = Article.objects.filter(id=product_id)
    db_logger.info(f"qs_product => {qs_product}")

    # product not exists
    if not qs_product.exists():
        db_logger.info("if not qs_product.exists()")
        return JsonResponse({"msg": "success"}, status=404)

    # product exists and form valid
    if qs_product.exists():
        try:
            db_logger.info("if qs_product.exists()")

            quantity = str(data['quantity'])
            cart.add(product=qs_product[0],
                     quantity=quantity,
                     )
            db_logger.info("product added to cart")

            if request.user.is_authenticated:
                # save cart to db
                save_cart_before_logout(request)

            return JsonResponse({"msg": "done", "cartLength": cart.__len__()}, status=200)

        except Exception as e:
            db_logger.exception(f"erreur cart/cart_add => {e}")
            return JsonResponse({"msg": "clear"}, status=500)
