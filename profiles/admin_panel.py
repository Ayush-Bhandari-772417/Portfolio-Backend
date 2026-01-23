# apps/profiles/admin_panel.py
from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("headline", "short_intro", "about_text")
    list_display = ("name", "headline", "is_public", "updated_at")
