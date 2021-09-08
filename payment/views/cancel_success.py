from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.views.generic.base import View
from order.models import Order
import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic.base import View
from cart.models import CartNotFinalized
from cart.order_process import order_process
from order.pdf_generator import PDFGenerator
from payment.functions import send_mail_to_user, remove_file
from order.models import Order
from django.contrib import messages
from account.models import CustomUser, Address

from order.pdf_generator import PDFGenerator

db_logger = logging.getLogger('db')


class SuccessView(View):
    def get(self, *args, **kwargs):
        try:
            db_logger.info("DEBUT payment/cancel_success/Success")
            # get url args
            user_id = self.request.GET.get('u_id')
            order = self.request.GET.get('o_id')
            db_logger.info(f'user: {user_id}, order: {order}')
            db_logger.info(f'types user: {type(user_id)}, order: {type(order)}')

            # get user
            user = CustomUser.objects.get(id=int(user_id))

            # get order
            order: Order = Order.objects.get(
                user=self.request.user,
                status="PendingPayment"
            )
            db_logger.info(f"commande trouvée: {order}")

            # change status order
            order.status = "Paid"
            # order.stripe_id = rst_stripe['id']
            # order.stripe_payment_intent = checkout_session['payment_intent']
            # order.amount = order.get_total_cost()
            order.save()
            db_logger.info("status order changed")

            pdf = PDFGenerator().build_pdf(user, order)  # build pdf
            db_logger.info(f"pdf généré: {pdf}")
            send_mail_to_user(order, user, pdf)  # send to mail
            remove_file(pdf)  # remove_file in directory
            db_logger.info(f"fichier supprimé")

            self.request.session['cart'] = {}  # reinitialize cart session
            self.request.session.modified = True  # save changes in session db
            db_logger.info(f"variable session panier modifiée")

            # get cart not finalized and suppress it
            qs_cart = CartNotFinalized.objects.filter(user=int(self.request.user.id))
            if qs_cart.exists():
                db_logger.info(f"panier trouvé: {qs_cart[0]}")
                qs_cart[0].delete()
                db_logger.info(f"panier supprimé")
            else:
                db_logger.warning(f"pas de panier trouvé (l 54: payment/order_without_payment)")

            messages.success(self.request, 'Votre commande a bien été passée')
            db_logger.info("FIN payment/cancel_success")
            return redirect("order:order_detail", pk=order.id)
        except Exception as e:
            db_logger.exception(f"payment/cancel_success/Success => {e}")
            messages.error(self.request, 'Erreur lors du passage de votre commande')
            return redirect("cart:cart_detail")


class CancelView(TemplateView):
    template_name = "payment/cancel.html"
