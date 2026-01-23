# apps/hires/models.py
from django.db import models

class HiringMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    details = models.TextField()
    stipend = models.CharField(max_length=20, blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    # Optional fields for security / analytics
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.name} - {self.email}"
