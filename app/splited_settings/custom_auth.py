"""
Custom authentication
 """

AUTH_USER_MODEL = 'account.CustomUser'  # custom user

AUTHENTICATION_BACKENDS = [
    'account.backends.MyModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'account:register'
