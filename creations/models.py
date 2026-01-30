# apps/creations/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_public = models.BooleanField(default=True)
    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Creation(models.Model):
    LANGUAGE_CHOICES = (
        ("en", _("English")),
        ("ne", _("Nepali")),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_public = models.BooleanField(default=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default="en")

    # Translation grouping
    translation_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )

    featured_image = models.ImageField(upload_to="feature_images/", blank=True, null=True)
    featured_image_alt = models.CharField(max_length=255, blank=True)

    TYPE_CHOICES = [
        ('blog', 'Blog'),
        ('poem', 'Poem'),
        ('story', 'Story'),
        ('article', 'Article'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="creations"
    )

    keywords = models.JSONField(default=list, blank=True)
    excerpt = models.TextField()

    written_date = models.DateField()
    published_date = models.DateField(null=True, blank=True)
    published_in = models.CharField(max_length=255, null=True, blank=True)

    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="editor"
    )
    
    # NEW: Tiptap-based content fields
    content_json = models.JSONField(null=True, blank=True)   # Raw Tiptap JSON (ProseMirror)
    content_html = models.TextField(null=True, blank=True)   # Render-ready HTML version

    class Meta:
        ordering = ['-written_date', '-posted_date']

    def __str__(self):
        return f"{self.title} ({self.type})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    
@receiver(post_delete, sender=Creation)
def delete_featured_image(sender, instance, **kwargs):
    if instance.featured_image:
        instance.featured_image.delete(save=False)
