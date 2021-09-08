from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.views.generic.base import View

from account.forms import UserPasswordResetForm
from account.functions import password_reset_token

User = get_user_model()


class ResetPasswordView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None
        if user is not None and password_reset_token.check_token(user, token):
            context = {
                'form': UserPasswordResetForm(user),
                'uid': uidb64,
                'token': token
            }
            return render(request, 'reset_password/reset_confirm.html', context)
        else:
            messages.add_message(request, messages.WARNING, 'Le lien est invalide')
            messages.add_message(request, messages.WARNING, "S'il vous plaît faîtes une nouvelle demande")

        return redirect('website:home')

    def post(self, request, uidb64, token):
        if request.method == 'POST':
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
                messages.add_message(request, messages.WARNING, str(e))
                user = None

            if user is not None and password_reset_token.check_token(user, token):
                form = UserPasswordResetForm(user=user, data=request.POST)
                if form.is_valid():
                    # if form.is_valid() and request.recaptcha_is_valid:
                    form.save()
                    update_session_auth_hash(request, form.user)
                    user.is_active = True
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Mot de passe mis à jour !')
                    return redirect('website:home')
                else:
                    print(form.errors)
                    print(form.error_messages)
                    context = {
                        'form': form,
                        'uid': uidb64,
                        'token': token
                    }
                    messages.add_message(request, messages.WARNING, 'Vérifiez que vous respectez les règles du MDP')
                    return render(request, 'website/home.html', context)
            else:
                messages.add_message(request, messages.WARNING, 'Le lien est invalide')
                messages.add_message(request, messages.WARNING, "S'il vous plaît faîtes une nouvelle demande")
