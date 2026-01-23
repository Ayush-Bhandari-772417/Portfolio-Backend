# apps/qualifications/apps.py
from django.apps import AppConfig

class QualificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qualifications'
    
    def ready(self):
        import qualifications.admin_panel  # ✅ ensures admin models get registered
        