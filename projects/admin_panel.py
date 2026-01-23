# apps/projects/admin_panel.py
from django.contrib import admin
from .models import Project

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "started_date", "completed_date")
    search_fields = ("title", "description")
    list_filter = ("created_at", "updated_at", "started_date", "completed_date")
