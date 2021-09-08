from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('add_favorites/', add_favorites, name='add_favorites'),
    path('update/', cart_update, name='cart_update'),
    path('cart_remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
    path('get_total_with_delivery/', get_price_with_delivery, name='get_total_with_delivery'),
    path('leave_message/', leave_message, name='leave_message'),
]
