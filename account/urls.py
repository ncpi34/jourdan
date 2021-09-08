from . import views
from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('update_profile/', ProfileUpdateView.as_view(), name='update_profile'),

    path('update_address/', AddressUpdateView.as_view(), name='update_address'),


    path('register/', RegisterPartView.as_view(), name='register'),

    # activation
    path('activation_sent/', activation_sent, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', ActivateAccountView.as_view(), name='activate'),

    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('password_reset_confirm/<uidb64>/<token>/',
         ResetPasswordView.as_view(),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         views.PasswordResetCompleteView.as_view(template_name='reset_password/password_reset_complete.html'),
         name='password_reset_complete'),
]
