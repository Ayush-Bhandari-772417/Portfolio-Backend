# apps/skills/apps.py
from django.apps import AppConfig

class SkillConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skills'
    
    def ready(self):
        import skills.admin_panel  # ✅ ensures admin models get registered
        