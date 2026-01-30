# apps/settings/models.py
from django.db import models
from django.conf import settings

# Create your models here.

class Setting(models.Model):
    type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('textarea', 'Textarea'),
            ('boolean', 'Boolean'),
            ('number', 'Number'),
            ('color', 'Color'),
        ]
    )
    key = models.CharField(max_length=100, unique=True)         # site_title        footer_text     enable_blog     theme_color
    value = models.TextField()                                  # Ayush Bhandari    © 2025 Ayush    true            #1e40af
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.key


class SEOPageSetting(models.Model):
    PAGE_CHOICES = (
        ("home", "Home"),
        ("projects", "Projects"),
        ("project_detail", "Project Detail"),
        ("creations", "Creations"),
        ("creations_category", "Creations Category"),
        ("creations_type", "Creations Type"),
        ("creation_detail", "Creation Detail"),
        ("experience", "Experience"),
        ("skills", "Skills"),
        ("qualifications","Qualifications"),
        ("services", "Services"),
    )
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)   # home      project_detail      creation_detail
    index = models.BooleanField(default=True)                                   # true      true                false
    follow = models.BooleanField(default=True)                                  # true      true                false
    is_public = models.BooleanField(default=True)
    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.page


class SitemapSetting(models.Model):
    CHANGEFREQ_CHOICES = (
        ("always", "Always"),
        ("hourly", "Every hour"),
        ("daily", "Every day"),
        ("weekly", "Every week"),
        ("monthly", "every month"),
        ("yearly", "every year"),
        ("never", "Never"),
    )
    PAGE_CHOICES = (
        ("home", "Home"),
        ("projects", "Projects"),
        ("project_detail", "Project Detail"),
        ("creations", "Creations"),
        ("creations_category", "Creations Category"),
        ("creations_type", "Creations Type"),
        ("creation_detail", "Creation Detail"),
        ("experience", "Experience"),
        ("skills", "Skills"),
        ("qualifications","Qualifications"),
        ("services", "Services"),
    )
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)                                       # home      projects        skills
    include = models.BooleanField(default=True)                                                 # true      true            false
    priority = models.FloatField(default=0.5)                                                   # 1.0       0.8             0.3
    changefreq = models.CharField(max_length=20, choices=CHANGEFREQ_CHOICES, default="weekly")  # daily     weekly          monthly
    is_public = models.BooleanField(default=True)
    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.page


class DisplaySetting(models.Model):
    CONTEXT_CHOICES = (
        ("home", "Home Page"),
        ("portfolio", "Portfolio Page"),
        ("project", "Project"),
        ("project_category", "Project Category"),
        ("creation_page", "Creation Page"),
        ("creations_category", "Creations Category"),
        ("creations_type", "Creations Type"),
    )
    ITEM_CHOICES = (
        ("creations", "Creations"),
        ("experience", "Experience"),
        ("project", "Project"),
        ("qualifications","Qualifications"),
        ("services", "Services"),
        ("skills", "Skills"),
        ("socialmedias", "Social Medias"),
    )
    context = models.CharField(max_length=50, choices=CONTEXT_CHOICES)      # home      home        portfolio       project_category
    item_type = models.CharField(max_length=50, choices=ITEM_CHOICES)       # projects  skills      projects        projects
    limit = models.PositiveIntegerField(default=6)                          # 6         8           12              9
    is_public = models.BooleanField(default=True)
    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        unique_together = ("context", "item_type")

    def __str__(self):
        return f"{self.context} - {self.item_type}"
