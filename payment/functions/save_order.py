import os
from typing import IO
from account.backends import User
from cart.cart import Cart
from website.models import Article, FavoritesClient
from order.models import OrderItems, Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import logging

db_logger = logging.getLogger('db')


def save_order(cart: Cart, order: Order, user: User):
    """
    Save order
    """

    db_logger.info("DEBUT payment/functions/save_order")
    for item in cart:
        article = Article.objects.filter(id=int(item['article_id']))
        if article.exists():

            db_logger.info("article existe")
            item_order: OrderItems = OrderItems(
                order=order,
                quantity=item['quantity'],
                article_code=item['article_code'],
                price_with_taxes=item['price_with_taxes'],
                name=item['name'],
                price_type=item['price_type']

            )
            db_logger.info(f"item_order => {item_order}")
            item_order.save()

            # add favorites products for user
            favorites, created = FavoritesClient.objects.get_or_create(
                user=user,
                article=article[0]
            )
            # add quantity to favorites
            qty = 1
            try:
                qty = int(item['quantity'])
            except:
                pass

            favorites.quantity += qty
            favorites.save()
            db_logger.info(f"favorites => {favorites}")
        else:
            db_logger.info(f"article n'existe pas => {article}")
    db_logger.info("FIN payment/functions/save_order")
    return True


def send_mail_to_user(order: Order, user: User, pdf: IO):
    """
    Send mail to user
    Args:
        order: db object
        user:  db object
        pdf: file

    Returns: void

    """
    message = render_to_string('mail/order_email.html', {
        'user': user,
        'order': order,
        'domain': settings.CURRENT_SITE
    })

    tab_mails = [settings.DELIVERY_MAIL]
    if user.email is not None:
        tab_mails.append(user.email)
    email = EmailMessage(
        'Commande effectuée sur le site internet',
        message,
        settings.EMAIL_HOST_USER,
        tab_mails
    )

    email.attach_file(pdf)
    email.send(fail_silently=True)


def remove_file(path: str):
    """
    Remove file
    Args:
        path: str

    Returns: void

    """
    if os.path.exists(path):
        os.remove(path)
