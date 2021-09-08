import json
from django.views.decorators.http import require_POST
from cart.cart import Cart
from website.models import Article
from django.http import JsonResponse
import logging

db_logger = logging.getLogger('db')


def add_to_cart(qs_product, quantity, cart):
    db_logger.info("FIN cart/add_favorites add_to_cart")
    # product exists
    if qs_product.exists():
        db_logger.info(f"if qs_product.exists() => {qs_product[0]}")
        # quantity is enough
        if qs_product[0].stock > 0:
            db_logger.info("if qs_product.first.stock > 0")
            # quantity less than stock
            if quantity <= qs_product[0].stock:
                db_logger.info("if cd['quantity'] <= qs_product.first.stock")
                cart.add(product=qs_product[0],
                         quantity=quantity,
                         )

            # quantity more than stock
            else:
                db_logger.info("in else if cd['quantity'] <= qs_product.first.stock")
                cart.add(product=qs_product[0],
                         quantity=qs_product[0].stock,
                         )
        db_logger.info("FIN cart/add_favorites add_to_cart")
    else:
        db_logger.warning(f"produit non trouvé => {qs_product[0]}")


@require_POST
def add_favorites(request):
    """
    Add multiple favorites to cart
    """
    try:
        db_logger.info("DEBUT cart/add_favorites")
        data: dict = json.loads(request.body)  # get json body
        # get cart
        cart: Cart = Cart(request)
        db_logger.info(f"cart => {cart}")

        # adding articles to cart
        for item in data:
            qs_product: [Article] = Article.objects.filter(id=int(item['article']))
            add_to_cart(qs_product, int(item['quantity']), cart)
            db_logger.info(f"qs_product => {qs_product}")

        db_logger.info("FIN cart/add_favorites")
        return JsonResponse({"msg": "success"}, status=200)

    except Exception as e:
        db_logger.exception(f"erreur cart/cart_add => {e}")
        return JsonResponse({"msg": "error"}, status=500)
