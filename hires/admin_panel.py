# apps/hires/admin_panel.py
from django.contrib import admin
from .models import HiringMessage

# Register your models here.

@admin.register(HiringMessage)
class HiringMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "posted_at")
    search_fields = ("name", "email", "phone", "details")
    list_filter = ("posted_at",)
