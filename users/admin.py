from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("email", "first_name", "last_name", "avatar", "birth_date",  "is_staff", "is_active", "is_superuser")
    list_filter = ("email", "first_name", "last_name", "avatar", "birth_date",  "is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "avatar", "birth_date", 'password')}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "avatar", "birth_date",  "is_staff", "is_active",
                       "is_superuser")}),
    )
    search_fields = "email",
    ordering = "email",


admin.site.register(User, CustomUserAdmin)
