from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["id", "username", "email", "first_name",
                    "last_name", "is_active", "is_staff", "is_superuser"]
    list_display_links = ["id", "username"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["username", "email", "first_name", "last_name"]
    readonly_fields = ["ips"]
    ordering = ["-date_joined"]

    fieldsets = (
        (None, {'fields': ('username', 'password', 'ips')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
