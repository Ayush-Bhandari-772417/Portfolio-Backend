# apps/creations/apps.py
from django.apps import AppConfig

class CreationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'creations'
    
    def ready(self):
        import creations.admin_panel  # ✅ ensures admin models get registered
        