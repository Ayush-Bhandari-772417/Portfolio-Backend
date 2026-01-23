# apps/services/apps.py
from django.apps import AppConfig

class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'
    
    def ready(self):
        import services.admin_panel  # ✅ ensures admin models get registered
        
