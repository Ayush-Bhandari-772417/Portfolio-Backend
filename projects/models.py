# apps/projects/models.py
from django.db import models
from users.models import User
from django.conf import settings

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    # Basic Details
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    excerpt = models.TextField()
    abstract = models.TextField()

    # Structured Lists
    features = models.JSONField(default=list, blank=True)
    technologies = models.JSONField(default=list, blank=True)
    keywords = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)

    # Media
    featured_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    featured_image_alt = models.CharField(max_length=255, blank=True)

    # Links
    repository_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    demo = models.URLField(blank=True, null=True)

    # Team
    contributors = models.JSONField(default=list, blank=True)

    # Status
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')

    PROJECT_TYPE = [
        ('academic', 'Academic Project'),
        ('personal', 'Personal Project'),
        ('client', 'Freelance / Client'),
    ]
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE, default='personal')

    is_public = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    client_feedback = models.TextField(blank=True, null=True)

    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    # Dates
    started_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Analytics
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-started_date']   # or '-completed_date'

    def __str__(self):
        return self.title

    @property
    def duration(self):
        if self.started_date and self.completed_date:
            return (self.completed_date - self.started_date).days
        return None

# New: Dedicated Gallery Image model
class ProjectGallery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.project.title} - {self.caption or 'Image'}"