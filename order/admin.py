from django.contrib import admin
from order.models import Order, OrderItems
import logging
from django.utils import timezone
from cart.models import CartNotFinalized
from order.pdf_generator import PDFGenerator
from payment.functions import send_mail_to_user, remove_file
from order.models import Order

db_logger = logging.getLogger('db')


class OrderItemsInLine(admin.TabularInline):
    model = OrderItems
    readonly_fields = (
        'article_code', 'price_with_taxes', 'quantity')
    fields = ('article_code', 'price_with_taxes', 'quantity')


@admin.register(Order)
class OrderViews(admin.ModelAdmin):
    list_display = ['id', 'date', 'user', 'get_total_cost', 'status', 'message']
    list_filter = ['date']
    date_hierarchy = 'date'
    inlines = [OrderItemsInLine]
    exclude = (
        'stripe_id', 'coupon', 'delivery_date', 'shipping_address', 'billing_address', 'delivery_price',
        'payment', 'refund_requested')
    search_fields = ('user__username',)
    ordering = ('status',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all()

    # handle permissions
    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


# @admin.register(OrderItems)
# class OrderItemsViews(admin.ModelAdmin):
#     list_display = ('id', 'article_code', 'quantity',)
#     readonly_fields = ('id', 'article_code', 'quantity',)
#     list_filter = ('order__date',)
#
#     # handle permissions
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_add_permission(self, request):
#         return False
