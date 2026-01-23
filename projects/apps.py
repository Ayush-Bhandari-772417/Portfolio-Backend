# apps/projects/apps.py
from django.apps import AppConfig

class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'
    
    def ready(self):
        import projects.admin_panel  # ✅ ensures admin models get registered
        