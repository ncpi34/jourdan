from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenVerifyView
)

app_name = 'apiCashRegister'

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = [

    # novelties
    path('novelties/', NoveltiesList.as_view()),
    path('noveltie/<int:pk>/', NoveltiesDetail.as_view()),

    # auth
    path('login/', MyTokenObtainPairView.as_view(), name='token_create'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += router.urls
