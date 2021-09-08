from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from account.functions.tokens import account_activation_token


def custom_send_mail(request, user, subject, template):
    current_site = get_current_site(request)  # not working on local
    current_site = request.get_host()

    message = render_to_string(template, {
        'user': user,
        # 'domain': current_site.domain,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        # method will generate a hash value with user related data
        'token': account_activation_token.make_token(user),
        'protocol': 'https',
    })
    user.email_user(subject, message)
