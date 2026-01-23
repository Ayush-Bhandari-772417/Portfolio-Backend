# apps/services/admin/models.py
from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=100)                        # e.g., "Freelancing", "AI/ML"
    description = models.TextField()
    icon = models.CharField(max_length=255, blank=True, null=True)  # optional: CSS class, SVG, or icon URL
    is_public = models.BooleanField(default=True)                   # show/hide on public API
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
