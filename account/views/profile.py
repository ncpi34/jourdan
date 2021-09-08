from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import CustomUser
import logging

db_logger = logging.getLogger('db')


class ProfileView(LoginRequiredMixin, View):
    """
    Profile
    """

    def get(self, request, *args, **kwargs):
        db_logger.info("DEBUT account/profile ProfileView")
        try:
            user = get_object_or_404(CustomUser, pk=request.user.id)
            db_logger.info(f"user => {user}")
            db_logger.info("FIN account/profile ProfileView")
            return render(request, 'account/profile.html', {'user': user})

        except Exception as e:
            db_logger.exception(f"erreur account/profile ProfileView => {e}")
            messages.error(request, "Vous n'avez pas accès à cette partie du site")
            return redirect('website:products')
