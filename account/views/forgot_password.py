from django.contrib import messages
from django.contrib.auth.views import PasswordContextMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
import json
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from account.functions import custom_send_mail
from account.models import CustomUser
import logging

db_logger = logging.getLogger('db')


class ForgotPasswordView(View):
    """
    Password forgot
    """

    def post(self, request) -> json:
        db_logger.info("DEBUT account/forgot_password ForgotPasswordView")
        # get json
        req: dict = json.loads(request.body)
        db_logger.info(f"req => {req}")
        if req['forgot_pass_email']:
            # get data
            mail: str = req['forgot_pass_email']
            db_logger.info(f"mail => {mail}")
            try:
                db_logger.info("dans le try")

                # get user
                user: CustomUser = CustomUser.objects.get(email=mail)
                db_logger.info(f"user => {user}")

                # send mail
                subject: str = 'Réinitialisation de votre mot de passe'
                template: str = 'mail/reset_password_email.html'
                custom_send_mail(self.request, user, subject, template)
                db_logger.info("envoi du mail effectue")

                message = 'Vous allez recevoir un email contenant les instructions à suivre'
                db_logger.info("DEBUT account/forgot_password ForgotPasswordView")
                return JsonResponse({"msg": message}, status=201)
            except Exception as e:
                message = "Nous ne parvenons pas à vous envoyer un email"
                db_logger.exception(f"erreur account/forgot_password ForgotPasswordView => {e}")
                return JsonResponse({"err": message}, status=400)
        else:
            message = "Veuillez rentrer un email valide"
            db_logger.error(f"erreur account/forgot_password ForgotPasswordView email non valide => {req}")
            return JsonResponse({"err": message}, status=400)


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        db_logger.info("DEBUT account/forgot_password PasswordResetCompleteView get_context_data")
        try:
            # update ctx
            context = super().get_context_data(**kwargs)
            db_logger.info("FIN account/forgot_password PasswordResetCompleteView")
            return context
        except Exception as e:
            db_logger.exception(f"erreur account/forgot_password PasswordResetCompleteView => {e}")

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Votre mot de passe a été mis à jour')
        db_logger.info("FIN account/forgot_password PasswordResetCompleteView")
        return redirect('website:products')
