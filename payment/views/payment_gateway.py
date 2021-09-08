import stripe
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import View
from account.models import CustomUser, Address
from cart.order_process import order_process
from order.models import Order, OrderItems
import logging

from payment.models import Stripe

db_logger = logging.getLogger('db')


class PaymentGatewayView(LoginRequiredMixin, View):
    """
    Payment Canceled View
    only http post allow
    No login required
    """

    @staticmethod
    def get_stripe_keys():
        stripe_keys: [Stripe] = Stripe.objects.all()
        public_key = stripe_keys.first().public_key
        private_key = stripe_keys.first().private_key
        return {'public': public_key, 'private': private_key}

    def post(self, *args, **kwargs):
        """ post """
        db_logger.info("DEBUT payment/payment_gateway")
        try:
            db_logger.info(f"dans le premier try")

            # get user
            user: CustomUser = CustomUser.objects.get(id=self.request.user.id)
            db_logger.info(f"utilisateur trouvé: {user}")

            # get order
            order: Order = Order.objects.get(user=self.request.user, status="PendingPayment")
            db_logger.info(f"commande trouvée: {order}")

            # get user address
            address = Address.objects.filter(user=self.request.user)

            # save order to db
            order = order_process(self.request)
            db_logger.info("recuperation ou creation commande")

            # change order date & status
            order.date = timezone.now()
            order.save()
            db_logger.info(f"sauvegarde commande effectuée")

            # format amount
            amount = int(order.get_total_cost() * 100)
            db_logger.info(f"amount: {amount}")

            # get items
            items: [OrderItems] = OrderItems.objects.filter(order=order)

            # # create empty dict
            # items_dict: {} = {}
            # if items.exists():
            #     # append values to list
            #     for i in items:
            #         items_dict.update({
            #             i.id: {
            #                 'price_data': {
            #                     'currency': 'eur',
            #                     'product_data': {
            #                         'name': i.name,
            #                     },
            #                     'unit_amount': int(round(i.price_with_taxes * 100, 2)),
            #                     'quantity': i.quantity
            #                 }
            #             }
            #         })
            # db_logger.info(f"items_list: {items_dict}")

            # get keys
            keys: dict = self.get_stripe_keys()
            private_key = keys['private']

            # update api key stripe
            stripe.api_key = private_key
            print(int(round(order.get_total_cost() * 100, 2)))

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': "total",
                            },
                            'unit_amount': int(round(order.get_total_cost() * 100, 2)),
                        },
                        # 'amount_total': int(round(order.get_total_cost() * 100, 2)),
                        'quantity': 1,
                    }
                ],
                payment_method_types=[
                    'card',
                ],
                # amount_total=1000,
                # order.get_total_cost() * 100
                mode='payment',
                # dict optionnal infos
                # metadata=items_dict,
                # user

                client_reference_id=user.id,
                customer_email=user.email,
                success_url=self.request.build_absolute_uri(reverse('payment:success_payment') + f"?u_id={user.id}&o_id={order.id}"
                                                            ),
                cancel_url=self.request.build_absolute_uri(reverse('payment:cancel_payment')),
            )
            db_logger.info(f"checkout session: {checkout_session}")

            return redirect(checkout_session.url)
        except Exception as e:
            db_logger.exception(f"err payment/payment_gateway POST => {e}")
            return redirect('payment:cancel_payment')
