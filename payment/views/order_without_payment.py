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
import logging

db_logger = logging.getLogger('db')


class OrderWithoutPayment(LoginRequiredMixin, View):
    """
    Order without payment
    only http get allow
    Login required
    """

    def get(self, *args, **kwargs):
        db_logger.info("DEBUT payment/order_without_payment")
        try:
            # get user
            user = CustomUser.objects.get(id=int(self.request.user.id))
            db_logger.info(f"utilisateur trouvé: {user}")

            # get order then change date & status(ordered)
            order: Order = Order.objects.get(
                user=user,
                status="PendingPayment"
            )
            db_logger.info(f"commande trouvée: {order}")

            # get user address
            address = Address.objects.filter(user=self.request.user)

            # save order to db
            order = order_process(self.request)
            db_logger.info("recuperation ou creation commande")

            # change order date & status
            order.date = timezone.now()
            order.status = "Ordered"
            order.save()
            db_logger.info(f"sauvegarde commande effectuée")

            pdf = PDFGenerator().build_pdf(user, order)  # build pdf
            db_logger.info(f"pdf généré: {pdf}")
            send_mail_to_user(self.request, order, user, pdf)  # send to mail
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
            db_logger.info("FIN payment/order_without_payment")
            return redirect("order:order_detail", pk=order.id)

        except Exception as e:
            db_logger.exception(f"erreur maj context (payment/order_without_payment)=> {e}")
            messages.error(self.request, "Votre commande n'a pas pu être éffectuée")
            return redirect("cart:cart_detail")
