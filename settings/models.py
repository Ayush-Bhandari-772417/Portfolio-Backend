# # apps/settings/models.py
# from django.db import models
# from django.conf import settings

# # Create your models here.

# class Setting(models.Model):
#     type = models.CharField(
#         max_length=20,
#         choices=[
#             ('text', 'Text'),
#             ('textarea', 'Textarea'),
#             ('boolean', 'Boolean'),
#             ('number', 'Number'),
#             ('color', 'Color'),
#         ]
#     )
#     key = models.CharField(max_length=100, unique=True)         # site_title        footer_text     enable_blog     theme_color
#     value = models.TextField()                                  # Ayush Bhandari    © 2025 Ayush    true            #1e40af
#     description = models.TextField(blank=True)
#     is_public = models.BooleanField(default=True)
#     uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
#     uploaded_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     def __str__(self):
#         return self.key


# class SEOPageSetting(models.Model):
#     PAGE_CHOICES = (
#         ("home", "Home"),
#         ("projects", "Projects"),
#         ("project_detail", "Project Detail"),
#         ("creations", "Creations"),
#         ("creations_category", "Creations Category"),
#         ("creations_type", "Creations Type"),
#         ("creation_detail", "Creation Detail"),
#         ("experience", "Experience"),
#         ("skills", "Skills"),
#         ("qualifications","Qualifications"),
#         ("services", "Services"),
#     )
#     page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)   # home      project_detail      creation_detail
#     crawl = models.BooleanField(default=True)                                   # true      true                false
#     index = models.BooleanField(default=True)                                   # true      true                false
#     follow = models.BooleanField(default=True)                                  # true      true                false
#     is_public = models.BooleanField(default=True)
#     uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
#     uploaded_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     def __str__(self):
#         return self.page


# class SitemapSetting(models.Model):
#     CHANGEFREQ_CHOICES = (
#         ("always", "Always"),
#         ("hourly", "Every hour"),
#         ("daily", "Every day"),
#         ("weekly", "Every week"),
#         ("monthly", "every month"),
#         ("yearly", "every year"),
#         ("never", "Never"),
#     )
#     PAGE_CHOICES = (
#         ("home", "Home"),
#         ("projects", "Projects"),
#         ("project_detail", "Project Detail"),
#         ("creations", "Creations"),
#         ("creations_category", "Creations Category"),
#         ("creations_type", "Creations Type"),
#         ("creation_detail", "Creation Detail"),
#         ("experience", "Experience"),
#         ("skills", "Skills"),
#         ("qualifications","Qualifications"),
#         ("services", "Services"),
#     )
#     page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)                                       # home      projects        skills
#     include = models.BooleanField(default=True)                                                 # true      true            false
#     priority = models.FloatField(default=0.5)                                                   # 1.0       0.8             0.3
#     changefreq = models.CharField(max_length=20, choices=CHANGEFREQ_CHOICES, default="weekly")  # daily     weekly          monthly
#     is_public = models.BooleanField(default=True)
#     uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
#     uploaded_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     def __str__(self):
#         return self.page


# class DisplaySetting(models.Model):
#     CONTEXT_CHOICES = (
#         ("home", "Home Page"),
#         ("portfolio", "Portfolio Page"),
#         ("project", "Project"),
#         ("project_category", "Project Category"),
#         ("creation_page", "Creation Page"),
#         ("creations_category", "Creations Category"),
#         ("creations_type", "Creations Type"),
#     )
#     ITEM_CHOICES = (
#         ("creations", "Creations"),
#         ("experience", "Experience"),
#         ("project", "Project"),
#         ("qualifications","Qualifications"),
#         ("services", "Services"),
#         ("skills", "Skills"),
#         ("socialmedias", "Social Medias"),
#     )
#     context = models.CharField(max_length=50, choices=CONTEXT_CHOICES)      # home      home        portfolio       project_category
#     item_type = models.CharField(max_length=50, choices=ITEM_CHOICES)       # projects  skills      projects        projects
#     limit = models.PositiveIntegerField(default=6)                          # 6         8           12              9
#     is_public = models.BooleanField(default=True)
#     uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
#     uploaded_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     class Meta:
#         unique_together = ("context", "item_type")

#     def __str__(self):
#         return f"{self.context} - {self.item_type}"














from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .choices import (
    DisplayItem,
    DisplayLocation,
    SettingGroup,
    SettingType,
    SitePage,
    SitemapChangeFrequency,
)

class AuditModel(models.Model):
    """
    Abstract base model providing common audit fields.
    """

    is_public = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this record is exposed through the public API.",
    )

    uploaded_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address from which this record was created or last modified.",
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_uploaded",
        help_text="User responsible for the latest update.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this record was created.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this record was last modified.",
    )

    class Meta:
        abstract = True


class Setting(AuditModel):
    """
    Generic key-value configuration store.

    Examples
    --------
    group = Branding
    key   = site_name
    value = Ayush Bhandari

    group = Homepage
    key   = home_page_title
    value = Ayush Bhandari | Computer Engineer

    group = SEO
    key   = default_robots
    value = index,follow
    """

    group = models.CharField(
        max_length=30,
        choices=SettingGroup.choices,
        db_index=True,
        help_text="Logical group this setting belongs to.",
    )

    type = models.CharField(
        max_length=20,
        choices=SettingType.choices,
        default=SettingType.TEXT,
        help_text="Data type of the stored value.",
    )

    key = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique machine-readable setting key.",
    )

    value = models.TextField(
        blank=True,
        help_text="Stored value. Interpretation depends on the selected type.",
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description shown in the admin panel.",
    )

    class Meta:
        ordering = ("group", "key")
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
        indexes = [
            models.Index(fields=["group"]),
            models.Index(fields=["key"]),
            models.Index(fields=["is_public"]),
        ]

    def __str__(self):
        return f"{self.group} • {self.key}"
    

class SEOPageSetting(AuditModel):
    """
    SEO behaviour for each logical page type.
    """

    page = models.CharField(
        max_length=40,
        choices=SitePage.choices,
        unique=True,
        db_index=True,
        help_text="Logical page this SEO rule applies to.",
    )

    crawl = models.BooleanField(
        default=True,
        help_text=(
            "Allow search engines to crawl this page. "
            "Used by robots.txt generation."
        ),
    )

    index = models.BooleanField(
        default=True,
        help_text=(
            "Allow this page to appear in search results."
        ),
    )

    follow = models.BooleanField(
        default=True,
        help_text=(
            "Allow search engines to follow links found on this page."
        ),
    )
    robots_override = models.CharField(
        max_length=100,
        blank=True,
        help_text=(
            "Optional custom robots directives "
            "(e.g. max-image-preview:large)."
        ),
    )

    class Meta:
        ordering = ("page",)
        verbose_name = "SEO Page Setting"
        verbose_name_plural = "SEO Page Settings"

    def __str__(self):
        return self.get_page_display()
    

class SitemapSetting(AuditModel):
    """
    Sitemap configuration for each logical page type.
    """

    page = models.CharField(
        max_length=40,
        choices=SitePage.choices,
        unique=True,
        db_index=True,
        help_text="Logical page this sitemap rule applies to.",
    )

    include = models.BooleanField(
        default=True,
        help_text="Whether URLs of this page type should appear in sitemap.xml.",
    )

    priority = models.FloatField(
        default=0.5,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0),
        ],
        help_text="Sitemap priority (0.0–1.0).",
    )

    changefreq = models.CharField(
        max_length=20,
        choices=SitemapChangeFrequency.choices,
        default=SitemapChangeFrequency.WEEKLY,
        help_text="Suggested change frequency for search engines.",
    )

    class Meta:
        ordering = ("page",)
        verbose_name = "Sitemap Setting"
        verbose_name_plural = "Sitemap Settings"

    def __str__(self):
        return self.get_page_display()


class DisplaySetting(AuditModel):
    """
    Controls how many items of a particular type are displayed
    at a particular location in the website.
    """

    location = models.CharField(
        max_length=40,
        choices=DisplayLocation.choices,
        db_index=True,
        help_text="Where the content is displayed.",
    )

    item_type = models.CharField(
        max_length=40,
        choices=DisplayItem.choices,
        db_index=True,
        help_text="Type of content being displayed.",
    )

    display_limit = models.PositiveIntegerField(
        default=6,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        help_text="Maximum number of items to display.",
    )

    class Meta:
        unique_together = ("location", "item_type",)
        ordering = ("location", "item_type",)
        verbose_name = "Display Setting"
        verbose_name_plural = "Display Settings"

    def __str__(self):
        return (
            f"{self.get_location_display()} → "
            f"{self.get_item_type_display()} "
            f"({self.display_limit})"
        )