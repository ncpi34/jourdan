from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def send_mail_to_admin(user, address, template, type="part"):
    message = render_to_string(template, {
        'user': user,
        'address': address
    })

    email = EmailMessage(
        'Demande de création de compte',
        message,
        settings.EMAIL_HOST_USER,
        [settings.ACCOUNT_MAIL]
    )

    email.attach_file(user.ci.path)
    if type == "pro":
        email.attach_file(user.kbis.path)
    email.send(fail_silently=True)


def send_mail_to_user(user, template, domain):
    message = render_to_string(template, {
        'user': user,
        'domain': domain
    })

    email = EmailMessage(
        'Demande de création de compte',
        message,
        settings.EMAIL_HOST_USER,
        [user.email]
    )

    email.send(fail_silently=True)
