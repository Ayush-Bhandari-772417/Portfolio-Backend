# apps/subscription/models.py
from django.db import models

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    # Optional but useful for analytics/security
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
