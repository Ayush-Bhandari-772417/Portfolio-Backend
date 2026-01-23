# apps/experience/admin_panel.py
from django.contrib import admin
from .models import Experience

# Register your models here.
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "start_date", "end_date", "location")
    list_filter = ("start_date", "end_date", "location")
    search_fields = ("title", "organization", "responsibilities")