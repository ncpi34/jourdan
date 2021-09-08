from django.contrib import messages
from django.shortcuts import render, redirect
from cart.forms import CartCheckAllProductsForm, CartUpdateProductForm
from cart.cart import Cart
from order.models import Order
import logging

db_logger = logging.getLogger('db')


def cart_detail(request):
    """
    Cart Details
    """
    try:
        db_logger.info("DEBUT cart/detail")

        # local var
        order_id = None

        cart = Cart(request)  # get cart
        quantity = CartCheckAllProductsForm  # get form
        for item in cart:  # add form in each product
            item['update_quantity_form'] = CartUpdateProductForm(
                initial={'quantity': item['quantity'], 'update': True},
                auto_id=False)

        # get session key in cookies
        session = request.COOKIES.get("sessionid")
        db_logger.info(f"session => {session}")

        # if user is authenticated: create order with status & send boolean to template
        user_connected: bool = False
        if request.user.is_authenticated:
            qs_order = Order.objects.get_or_create(
                user=request.user,
                status="PendingPayment"
            )
            order_id = qs_order[0].id  # unique number
            user_connected = True

        response = render(request, 'cart/cart-detail.html', {'cart': cart,
                                                             'quantity': quantity,
                                                             'info': session,
                                                             'order': order_id,
                                                             'totalCart': cart.get_total_price(),
                                                             'userConnected': user_connected
                                                             })
        db_logger.info(f"response => {response}")
        db_logger.info("FIN cart/detail")
        return response
    except Exception as e:
        db_logger.exception(f"erreur maj context (cart/detail)=> {e}")
        messages.error(request, "Une erreur est survenue")
        return redirect('website:home')
