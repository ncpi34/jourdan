from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from account.forms import AddressCreationForm
from account.models import Address
import logging

db_logger = logging.getLogger('db')


class AddressUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    Update address user
    """

    # specify the model you want to use
    model = Address

    # form from model
    form_class = AddressCreationForm

    # template
    template_name = 'account/address.html'

    # to redirect
    success_url = reverse_lazy("account:profile")

    # get user's address
    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)

    # if form valid send message
    def form_valid(self, form):
        messages.success(self.request, "Adresse mise à jour")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
