from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from account.forms import CustomUserUpdateForm
from account.models import CustomUser
import logging

db_logger = logging.getLogger('db')


class ProfileUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    Update profile user
    """

    # specify the model you want to use
    model = CustomUser

    # form from model
    form_class = CustomUserUpdateForm

    # template
    template_name = 'account/personal_info.html'

    # to redirect
    success_url = reverse_lazy("account:profile")

    # get user
    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.request.user.id)

    # if form valid send message
    def form_valid(self, form):
        messages.success(self.request, "Profil mis à jour")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
