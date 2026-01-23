# apps/creations/admin_panel.py
from django.contrib import admin
from .models import Creation, Category

# Register your models here.

@admin.register(Creation)
class CreationAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "user", "posted_date", "published_date")
    list_filter = ("type", "posted_date", "published_date")
    search_fields = ("title",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
