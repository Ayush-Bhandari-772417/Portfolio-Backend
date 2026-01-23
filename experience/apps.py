# apps/experience/apps.py
from django.apps import AppConfig

class ExperienceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'experience'
    
    def ready(self):
        import experience.admin_panel  # ✅ ensures admin models get registered
        