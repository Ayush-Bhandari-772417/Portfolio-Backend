# apps/settings/admin_panel.py
from django.contrib import admin
from .models import Setting, SEOPageSetting, SitemapSetting, DisplaySetting

# Register your models here.

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("type",)
    search_fields = ("type",)

@admin.register(SEOPageSetting)
class SEOPageSettingAdmin(admin.ModelAdmin):
    list_display = ("page",)
    search_fields = ("page",)

@admin.register(SitemapSetting)
class SitemapSettingAdmin(admin.ModelAdmin):
    list_display = ("page",)
    search_fields = ("page",)

@admin.register(DisplaySetting)
class DisplaySettingAdmin(admin.ModelAdmin):
    list_display = ("context",)
    search_fields = ("context",)