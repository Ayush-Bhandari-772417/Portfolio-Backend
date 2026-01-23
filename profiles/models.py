# apps/profiles/models.py
from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=50)           # HI! I'm
    headline = models.CharField(
        max_length=255,
        help_text="Short role/title e.g. Full Stack Developer"
    )
    short_intro = models.TextField(
        help_text="Hero section description"
    )
    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )
    profile_image_alt = models.CharField(max_length=100, blank=True)
    resume = models.FileField(
        upload_to="profile/",
        blank=True,
        null=True,
        help_text="Upload resume (PDF)"
    )
    resume_alt = models.CharField(max_length=100, blank=True)

    
    about_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )
    about_image_alt = models.CharField(max_length=100, blank=True)
    about_text = models.TextField(
        help_text="About section main text"
    )
    years_of_experience = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    
    logo = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )
    logo_alt = models.CharField(max_length=100, blank=True)
    named_logo = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )
    named_logo_alt = models.CharField(max_length=100, blank=True)

    keywords = models.JSONField(default=list, blank=True)
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.name
