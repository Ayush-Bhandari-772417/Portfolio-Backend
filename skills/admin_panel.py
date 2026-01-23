# apps/skills/admin_panel.py
from django.contrib import admin
from .models import Skill, SubSkill

# Register your models here.

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(SubSkill)
class SubSkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    