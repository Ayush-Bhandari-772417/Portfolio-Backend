# apps/qualifications/admin_panel.py
from django.contrib import admin
from .models import Qualification

# Register your models here.

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ("board_name", "school_name", "enrolled_year", "passed_year")
    search_fields = ("board_name", "school_name")
    list_filter = ("enrolled_year", "passed_year")
