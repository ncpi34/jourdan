from django.urls import path, include
from .views import *

app_name = 'payment'

urlpatterns = [
    path('order_without_payment/', OrderWithoutPayment.as_view(), name='order_without_payment'),
    path('payment/', PaymentGatewayView.as_view(), name='payment_gateway'),
    path('success/', SuccessView.as_view(), name='success_payment'),
    path('cancel/', CancelView.as_view(), name='cancel_payment'),
]
