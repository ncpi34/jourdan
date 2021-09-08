from django.contrib import admin
from account.models.custom_user import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from rest_framework.authtoken.models import Token
from .forms import CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'payment_enabled')
    list_filter = ('email', 'is_staff', 'is_active', 'payment_enabled')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'payment_enabled')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


# Unregister part
admin.site.unregister(Site)
admin.site.unregister(Token)
