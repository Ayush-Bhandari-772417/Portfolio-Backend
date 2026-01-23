# apps/subscription/apps.py
from django.apps import AppConfig

class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription'
    
    def ready(self):
        import subscription.admin_panel  # ✅ ensures admin models get registered