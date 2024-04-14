from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ['-date_joined']
    list_display = ['pk', 'username', 'first_name', 'last_name',
                    'email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login', 'date_joined',
                    'password']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    fieldsets = [
        (
            None,
            {
                "fields": ['username', 'password']
            }
        ),
        (
            _('Personal Info'),
            {
                'fields': ['first_name', 'last_name', 'email',]
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ['is_staff', 'is_active', 'is_superuser', 'groups',
                           'user_permissions']
            }
        ),
        (
            _('Important Dates'),
            {
                'fields': ['last_login', 'date_joined']
            }
        )
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff',
                       'is_active')}
         ),
    )
