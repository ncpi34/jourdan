from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from account.forms import CustomUserCreationForm, AddressCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
import logging

db_logger = logging.getLogger('db')


class RegisterPartView(SuccessMessageMixin, View):
    form = CustomUserCreationForm
    form_class_address = AddressCreationForm
    success_url = reverse_lazy('website:products')
    template_name = 'auth/register.html'
    success_message = 'Votre compte est désormais actif'

    def get(self, request):
        form = self.form(None)
        form_address = self.form_class_address(None)
        return render(request, self.template_name, {
            'form': form, 'form_address': form_address
        })

    def post(self, *args, **kwargs):
        form = self.form(self.request.POST)
        form_address = self.form_class_address(self.request.POST)
        if form.is_valid() and form_address.is_valid():
            user = form.save()
            address = form_address.save(commit=False)
            address.user = user

            user.is_complete = True
            user.is_active = True
            # check_unique_email(user, user.email)
            user.save()
            address.save()

            # send mail to admin
            # send_mail_to_admin(user, address, 'mail/register_part_mail_to_admin.html')

            """ link activation """
            # custom_send_mail(self.request, user, "Activez votre compte", 'mail/activation_request.html')
            """ send mail to notify creation account"""
            # send_mail_to_user(user, 'mail/profile_completed.html', self.request.get_host())

            messages.success(self.request, self.success_message)
            return redirect('website:home')

        messages.error(self.request, 'Veuillez bien remplir les champs')
        return render(self.request, self.template_name, {
            'form': form, 'form_address': form_address
        })
