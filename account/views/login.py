from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from account.forms import CustomAuthenticationForm
from account.functions.persistent_session_vars import PersistSessionVars
from django.utils.decorators import method_decorator
from cart.cart import Cart
from cart.models import CartNotFinalized
from order.models import Order
from website.models import Article
import logging

db_logger = logging.getLogger('db')


# persist session cart
@method_decorator(PersistSessionVars(['cart']), name='dispatch')
class LoginView(SuccessMessageMixin, View):
    """
    Login
    """
    form = CustomAuthenticationForm
    success_url = reverse_lazy('website:products')
    template_name = 'auth/login.html'
    success_message = 'Vous êtes connecté'

    def get(self, request):
        form = self.form(None)
        return render(request, self.template_name, {
            'form': form
        })

    def get_old_cart(self, *args, **kwargs):
        """ get cart not finalized and check if article exists"""
        db_logger.info("DEBUT account/login get_old_cart")

        # get cart in session
        cart_session = self.request.session['cart']

        db_logger.info("FIN account/login get_old_cart")

        # get cart
        cart = Cart(self.request)

        # get old cart
        old_cart = CartNotFinalized.objects.filter(user=self.request.user.id)
        db_logger.info(f"old_cart: {old_cart}")

        # if no cart old cart
        if not old_cart.exists():
            db_logger.info(f"no old cart")
            CartNotFinalized.objects.create(user=self.request.user.id, data=self.request.session.get('cart'))
            return

        # get data
        old_cart = old_cart.first().data

        for item in old_cart:
            qs = Article.objects.filter(article_code=old_cart[item]['article_code'])
            db_logger.info(f"article_code: {old_cart[item]['article_code']}")
            db_logger.info(f"type article_code: {type(old_cart[item]['article_code'])}")
            db_logger.info(f"qs: {qs}")

            # if article exists
            if qs.exists():
                db_logger.info(f"qs exists")
                try:
                    cart_session[item] = old_cart[item]

                    # # if article in session and db
                    # if cart_session[item]['article_code'] == old_cart[item]['article_code']:
                    #
                    #     # get qty session
                    #     quantity = cart_session[item]['quantity']
                    #
                    #     # add item to session
                    #     cart_session[item] = old_cart[item]
                    #
                    #     # apply qty session
                    #     cart_session[item]['quantity'] = quantity
                    # else:
                    #     # add item to session cart
                    #     cart_session[item] = old_cart[item]
                except Exception as e:
                    print(f"err login => {e}")
                    pass

        db_logger.info(f"cart_session: {cart_session}")

    def get_or_create_order(self):
        db_logger.info("DEBUT account/login get_or_create_order")
        order = Order.objects.get_or_create(
            user=self.request.user,
            status="PendingPayment",
        )
        order[0].save()
        db_logger.info("DEBUT account/login get_or_create_order")

    def post(self, request):
        db_logger.info("DEBUT account/login")

        form = self.form(self.request.POST)

        # get data
        req: [] = request.POST

        # extract data
        username = req["email"]
        password = req["password"]

        # if credentials
        if username and password:
            try:
                # authenticate
                user = authenticate(username=username, password=password)
                if user:
                    # login
                    login(request, user)
                    db_logger.info("utilisteur logge")

                    # get old cart
                    self.get_old_cart(user)
                    db_logger.info("recuperation ancien panier")

                    # get or create order
                    self.get_or_create_order()
                    db_logger.info("creation ou recuperation commande")

                    # flash msg
                    message = 'Bienvenue ' + request.user.email
                    db_logger.info("FIN account/login")

                    messages.success(self.request, message)
                    return redirect('website:home')
                else:
                    message = "Vous n'avez pas de compte"
                    messages.error(self.request, message)
                    return render(self.request, self.template_name, {
                        'form': form
                    })

            except Exception as e:
                message = 'Vos identifiants sont erronés'
                db_logger.exception(f"erreur account/login => {e}")
                messages.error(self.request, message)
                return render(self.request, self.template_name, {
                    'form': form
                })
