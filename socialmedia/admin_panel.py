# apps/socialmedia/admin_panel.py
from django.contrib import admin
from .models import SocialMedia

# Register your models here.

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "url")
    search_fields = ("name", "icon")
