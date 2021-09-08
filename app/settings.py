from pathlib import Path
import os
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
import app.tasks
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, 'app/.env.win'))

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = (os.getenv("DEBUG") == 'True')
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'widget_tweaks',
    'rest_framework',  # API
    'corsheaders',  # CORS
    'rest_framework.authtoken',  # token
    'mathfilters',  # mathfilters
    'django_countries',
    'tailwind',  # tailwind
    'theme',  # tailwind
    'cookie',  # cookie banner
    'user_visit',  # log users
    'crispy_forms',  # crispy forms

    "django.contrib.sites",
    "django.contrib.sitemaps",

    # applications
    'account.apps.AccountConfig',
    'cart',
    'order.apps.OrderConfig',
    'payment',
    'website.apps.WebsiteConfig',
    'log_db',
    'apiCashRegister',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'compression_middleware.middleware.CompressionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',  # in case of 404 send email
    'user_visit.middleware.UserVisitMiddleware',  # user visits
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Add the templates directory to the DIR option:
        "DIRS": [os.path.join(BASE_DIR, "templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'app.context_processors.get_current_domain',  # current domain
                'app.context_processors.cart',  # cart processor
                'app.context_processors.cart_length',  # cart_length processor
                'app.context_processors.homeTxt',  # delivery txt processor
                'app.context_processors.cgvFile',  # cgv processor
                'app.context_processors.harborCeilings',  # harborCeilings processor
                'website.functions.menus.get_menus',  # sidenav processor
                # "django.template.context_processors.i18n"  # i18n
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PWD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ('fr', _('French')),
    ('en-us', _('US English')),
]
USE_THOUSAND_SEPARATOR = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

""" Pagination """
DJANGO_TABLES2_PAGE_RANGE = 5

""" Crispy """
CRISPY_TEMPLATE_PACK = 'bootstrap4'

""" Caches """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cache_site'
    }
}

""" Email in case of problems """
# ADMINS = (
#     ('a.ledain', 'a.ledain@ncpi.fr'),
# )
# MANAGERS = ADMINS

""" Uploads limits """
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

"""Utf-8"""
DEFAULT_CHARSET = "utf-8"

"""Warning Default auto field"""
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# """ Stripe """
STRIPE_PUBLISHABLE_KEY = 'test_publishable_key'
STRIPE_SECRET_KEY = 'test_secret_key'
# STRIPE_LIVE_SECRET_KEY = os.getenv("STRIPE_LIVE_SECRET_KEY", "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")
# STRIPE_TEST_SECRET_KEY = os.getenv("STRIPE_TEST_SECRET_KEY", "sk_test_51HFFXAA3Nhh9FaEJXEAQ0jwtm9cL5rASFr62rcEanAPp7dSU6vDRg9F9lJcTctFWvgTO02nogSIkHHki7oJnE5F500gzdY609B")
# STRIPE_LIVE_MODE = False  # Change to True in production
# DJSTRIPE_WEBHOOK_SECRET = "whsec_Tr2osuGSbEDJvY4uaCwsAigCiKBhEjBR"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
# DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
# DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"  # Set to `"id"` for all new 2.4+ installations

"""Splitting settings"""
from app.splited_settings import *
from log_db.settings import LOGGING
