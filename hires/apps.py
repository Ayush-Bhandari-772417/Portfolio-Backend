# apps/hires/apps.py
from django.apps import AppConfig

class HireConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hires'
    
    def ready(self):
        import hires.admin_panel  # ✅ ensures admin models get registered
        