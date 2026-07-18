# apps/seo/choices.py

from django.db import models

class EventType(models.TextChoices):
    PAGE_VIEW = "page_view", "Page View"

    CLICK = "click", "Click"

    CTA_CLICK = "cta_click", "CTA Click"

    PROJECT_VIEW = "project_view", "Project View"

    SCROLL = "scroll", "Scroll"

    TIME = "time", "Time"

    FORM_SUBMIT = "form_submit", "Form Submit"

    DOWNLOAD = "download", "Download"

    OUTBOUND_LINK = "outbound_link", "Outbound Link"

    CUSTOM = "custom", "Custom"