from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from account.functions.tokens import account_activation_token
from account.models import CustomUser
import logging

db_logger = logging.getLogger('db')


def activation_sent(request):
    """
    Sent activation by mail
    """
    messages.success(request, 'Vérifiez vos mails pour activer votre compte')
    return redirect('website:products')
    # return render(request, 'auth/activation_request.html')  # This will activate user’s account


class ActivateAccountView(View):
    """
    Activate Account
    """

    def get(self, request, uidb64, token):
        db_logger.info("DEBUT account/activate")
        try:
            db_logger.info("dans le try")
            # decode token
            uid = force_text(urlsafe_base64_decode(uidb64))
            # get user
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            db_logger.exception("erreur account/activate => utilisateur n'existe pas")
            #user does not exists
            user = None
        # checking if the user exists, if the token is valid.
        if user is not None and account_activation_token.check_token(user, token):
            # user exists and token is fine
            db_logger.info("account/activate utilisateur existe")
            # activate account
            user.is_active = True
            user.signup_confirmation = True
            user.save()

            db_logger.info("account/activate utilisateur existe")
            # login
            login(request, user)
            # flash message
            messages.success(request, 'Bienvenue ' + request.user.email)
            db_logger.info("FIN account/activate")
            return redirect('website:products')

        else:
            #user not exists or error token
            messages.error(request, 'Activation invalide de votre compte')
            db_logger.error("erreur account/activate => activation invalide de votre compte")
            return redirect('website:products')
