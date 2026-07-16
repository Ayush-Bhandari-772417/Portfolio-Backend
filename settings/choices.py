# apps/settings/choices.py

from django.db import models


# ============================================================
# Generic Setting Types
# ============================================================

class SettingType(models.TextChoices):
    TEXT = "text", "Text"
    TEXTAREA = "textarea", "Textarea"
    BOOLEAN = "boolean", "Boolean"
    NUMBER = "number", "Number"
    COLOR = "color", "Color"


# ============================================================
# Website Pages
# These identifiers are used everywhere:
# • SEO settings
# • Sitemap settings
# • Metadata generation
# • robots.txt generation
# • sitemap.xml generation
# • Frontend page mappings
# ============================================================

class SitePage(models.TextChoices):
    HOME = "home", "Home"

    PROJECTS = "projects", "Projects"
    PROJECT_DETAIL = "project_detail", "Project Detail"

    CREATIONS = "creations", "Creations"
    CREATIONS_TYPE = "creations_type", "Creations Type"
    CREATION_DETAIL = "creation_detail", "Creation Detail"

    EXPERIENCE = "experience", "Experience Section"
    SKILLS = "skills", "Skills Section"
    QUALIFICATIONS = "qualifications", "Qualifications Section"
    SERVICES = "services", "Services Section"

    SITEMAP_HTML = "sitemap_html", "HTML Sitemap"

    NOT_FOUND = "not_found", "404 Page"


# ============================================================
# XML Sitemap Change Frequency
# https://www.sitemaps.org/protocol.html
# ============================================================

class SitemapChangeFrequency(models.TextChoices):
    ALWAYS = "always", "Always"
    HOURLY = "hourly", "Hourly"
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    YEARLY = "yearly", "Yearly"
    NEVER = "never", "Never"


# ============================================================
# Display Context
# Where the content is shown.
# ============================================================

class DisplayLocation(models.TextChoices):
    HOME = "home", "Homepage"

    PROJECT_LIST = "project_list", "Projects Listing"
    PROJECT_DETAIL = "project_detail", "Project Detail"

    CREATIONS = "creations", "Creations Listing"
    CREATIONS_TYPE = "creations_type", "Creations Type"
    CREATION_DETAIL = "creation_detail", "Creation Detail"


# ============================================================
# Display Item
# Which data is being displayed.
# ============================================================

class DisplayItem(models.TextChoices):
    PROJECTS = "projects", "Projects"
    CREATIONS = "creations", "Creations"
    EXPERIENCE = "experience", "Experience"
    SKILLS = "skills", "Skills"
    QUALIFICATIONS = "qualifications", "Qualifications"
    SERVICES = "services", "Services"
    SOCIAL_MEDIA = "social_media", "Social Media"


# ============================================================
# Generic Setting Groups
# Used to organize Setting entries in Django Admin.
# ============================================================

class SettingGroup(models.TextChoices):
    GENERAL = "general", "General"
    BRANDING = "branding", "Branding"
    CONTACT = "contact", "Contact"
    SOCIAL = "social", "Social"
    SEO = "seo", "SEO"
    ANALYTICS = "analytics", "Analytics"
    HOMEPAGE = "homepage", "Homepage"
    SECURITY = "security", "Security"
    FOOTER = "footer", "Footer"
    PERFORMANCE = "performance", "Performance"
    EMAIL = "email", "Email"
    API = "api", "API"
    OTHER = "other", "Other"