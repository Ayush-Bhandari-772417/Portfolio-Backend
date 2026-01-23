# apps/experience/models.py
from django.db import models

class Experience(models.Model):
    title = models.CharField(max_length=255)   # e.g., "Software Team"
    organization = models.CharField(max_length=255)  # e.g., "ECAST"
    organization_url = models.URLField(blank=True, null=True)  # optional external link

    location = models.CharField(max_length=255)  # e.g., "Thapathali Campus"
    location_url = models.URLField(blank=True, null=True)  # optional external link

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # null = Present

    responsibilities = models.JSONField(default=list)  # ["Coordinate software activities", "Organize trainings"]
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        if self.end_date:
            return f"{self.title} at {self.organization} ({self.start_date} – {self.end_date})"
        return f"{self.title} at {self.organization} ({self.start_date} – Present)"
