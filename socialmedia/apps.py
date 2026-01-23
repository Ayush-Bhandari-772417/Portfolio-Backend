# apps/socialmedia/apps.py
from django.apps import AppConfig

class SocialmedeiaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socialmedia'
    
    def ready(self):
        import socialmedia.admin_panel  # ✅ ensures admin models get registered
        