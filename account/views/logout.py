from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from account.functions.persistent_session_vars import PersistSessionVars
from account.models import CustomUser
from cart.models import CartNotFinalized
import logging

db_logger = logging.getLogger('db')


def save_cart_before_logout(request):
    """ Save cart before logout """
    db_logger.info("account/logout dans save_cart_before_logout")

    CartNotFinalized.objects.update_or_create(
        user=int(request.session.get('_auth_user_id')),
        defaults=dict(
            data=request.session.get('cart'), )
    )


# persist session cart
@PersistSessionVars(['cart'])
def logout_view(request):
    """
    Logout
    """
    db_logger.info("account/logout dans save_cart_before_logout")
    user = CustomUser.objects.get(id=request.user.id)
    if user:
        db_logger.info(f"user => {user}")
        try:
            db_logger.info(f"avant sauvegarde du panier")
            save_cart_before_logout(request)
            db_logger.info(f"apres sauvegarde du panier")
        except Exception as e:
            db_logger.exception(f"erreur account/logout dans save_cart_before_logout => {e}")

    logout(request)
    messages.warning(request, 'Vous êtes déconnecté')
    return redirect('website:products')
