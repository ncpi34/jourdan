from django.urls import path
from .views import *


app_name = 'order'

urlpatterns = [
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('order_detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('generate_pdf/<order_id>', PdfCreator.build_pdf, name='generate_pdf'),

]
