# apps/users/admin_panel.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("bio", "profile_image", "social_links")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
