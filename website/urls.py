from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'website'

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    url(r'^product/$', ArticleView.as_view(), name='products'),
    path('group/<int:group>/', ArticleView.as_view(model=Article), name='products_by_group'),
    path('family/<int:family>/', ArticleView.as_view(model=Article), name='products_by_family'),
    path('subfamily/<int:subfamily>', ArticleView.as_view(model=Article), name='products_by_subfamily'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='product_detail'),

    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('cancel_favorites/<int:pk>/', CancelFavoritesView.as_view(), name='cancel_favorites'),

    path('payment_condition/', PaymentConditionViews.as_view(), name='payment_condition'),
]
