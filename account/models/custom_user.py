from django.core.mail import send_mail
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(_('first name'), max_length=50, blank=True, null=True)
    first_name = models.CharField(_('last name'), max_length=50, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=255, unique=True,
                              error_messages={'unique': _("Un utilisateur avec cet email existe déjà"),
                                              }, )
    phone = models.CharField(_('phone'), max_length=10, validators=[MinLengthValidator(10)])
    is_complete = models.BooleanField(_('profile status'),
                                      default=False,
                                      help_text=_('Designates whether the user has a complete profile.'),
                                      )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    payment_enabled = models.BooleanField(_('paiment par CB'), default=True)

    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    signup_confirmation = models.BooleanField(default=False)
    one_click_purchasing = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = CustomUserManager()

    class Meta:
        app_label = 'account'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # unique_together = ('email', 'username',)
        # abstract = True

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs, fail_silently=False)


# @receiver(pre_save, sender=CustomUser)
# def check_duplicate_email(sender, **kwargs):
#     print('receiver customuser')
#     print('sender', sender)
#     print('kwargs', kwargs)
