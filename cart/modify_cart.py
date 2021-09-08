from django.core.exceptions import ObjectDoesNotExist
from order.models import Order, OrderItems
from website.models import Article, FavoritesClient
import datetime
from datetime import date
import uuid
from django.conf import settings
import logging

db_logger = logging.getLogger('db')


class RetrieveCart(object):
    """
    Retrieve Cart Class
    """

    @classmethod
    def get_unique_order(cls, request, args, dictionary=False):
        db_logger.info("in get_unique_order")
        status = None
        unique_number = None
        if not dictionary:
            db_logger.info("pas un dictionnaire")
            status = args
        else:
            db_logger.info("c'est un dictionnaire")
            # get keys of dict
            status = args['status']
            unique_number = args['unique_number']
        try:
            # find order
            order = Order.objects.get(user=request.user, status=status, unique_number=unique_number)
            print("order => ", order)
            db_logger.info(f"order => {order}")
            return order
        except ObjectDoesNotExist:
            # Object not exists
            db_logger.exception("commande non trouvee")
            return None

    @classmethod
    def get_or_create_order(cls, request, status):
        db_logger.info("in get_or_create_order")
        cart = request.session['cart']
        order = Order.objects.get_or_create(user=request.user, status=status)
        if order[0].unique_number is None:
            order[0].unique_number = cls.create_unique_str()
            order[0].save()
        """ create list of items """
        for item in cart:
            try:
                article = Article.objects.get(id=cart[item]['article_id'])
                item = OrderItems.objects.update_or_create(
                    order=order[0],
                    article=article,
                    defaults=dict(
                        quantity=cart[item]['quantity'], )
                )
            except ObjectDoesNotExist:
                order = Order.objects.get(user=request.user, status='PendingPayment')
                order.delete()
                settings.PRODUCT_DOES_NOT_EXISTS_ANYMORE = True

    @classmethod
    def delete_item_in_bdd(cls, request, product_id):
        db_logger.info("in delete_item_in_bdd")
        user = request.user
        if user.id is not None:
            order = Order.objects.get(user=user, status='PendingPayment')
            item_order = OrderItems.objects.get(article_id=product_id, order=order)
            item_order.delete()

    @classmethod
    def add_or_update_item_in_bdd(cls, request, product_id, quantity):
        db_logger.info("in add_or_update_item_in_bdd")
        user = request.user
        if user.id is not None:
            order = Order.objects.get_or_create(user=request.user, status='PendingPayment')

            if order[0].unique_number is None:
                order[0].unique_number = cls.create_unique_str()
                order[0].save()

            item_order = OrderItems.objects.get_or_create(article_id=product_id, order=order[0])
            item_order[0].quantity = quantity
            item_order[0].save()

    @staticmethod
    def create_unique_str():
        db_logger.info("in create_unique_str")
        # to format hour with minute
        now = datetime.datetime.now()
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        hour_with_minute = '{}{}'.format(hour, minute)

        # to format second with microsecond
        now = datetime.datetime.now()
        second = '{:02d}'.format(now.second)
        microsecond = str(now.microsecond // 1000)
        second_with_microsecond = '{}{}'.format(second, microsecond)

        file_name = '{}{}{}{}'.format(
            str(date.today()).replace('-', ''),
            hour_with_minute,
            second_with_microsecond,
            '.')
        unique = uuid.uuid4().hex[:20].upper()
        db_logger.info("FIN create_unique_str")
        return file_name + unique
