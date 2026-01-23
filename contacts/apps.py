# apps/contacts/apps.py
from django.apps import AppConfig

class ContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contacts'
    
    def ready(self):
        import contacts.admin_panel  # ✅ ensures admin models get registered
        