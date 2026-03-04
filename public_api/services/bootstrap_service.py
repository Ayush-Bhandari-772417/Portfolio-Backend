# apps/public_api/services/bootstrap_service.py
from django.db.models import Prefetch
from django.db import models

from profiles.models import Profile
from services.models import Service
from skills.models import Skill, SubSkill
from experience.models import Experience
from qualifications.models import Qualification
from socialmedia.models import SocialMedia
from settings.models import Setting, SEOPageSetting, SitemapSetting, DisplaySetting

class BootstrapService:

    @staticmethod
    def get_data():

        profile = Profile.objects.filter(is_public=True).first()

        skills = Skill.objects.filter(is_public=True).order_by("name").prefetch_related(
            Prefetch("subskills", queryset=SubSkill.objects.filter(is_public=True).order_by("name"))
        )

        return {
            "profile": profile,
            "services": Service.objects.filter(is_public=True).order_by("title"),
            "skills": skills,
            "experience": Experience.objects.filter(is_public=True).order_by(
                models.Case(
                    models.When(end_date__isnull=True, then=models.Value(0)),
                    default=models.Value(1),
                    output_field=models.IntegerField(),
                ),
                "-start_date",
            ),
            "qualifications": Qualification.objects.filter(is_public=True).order_by(
                models.Case(
                    models.When(passed_year__isnull=True, then=models.Value(0)),
                    default=models.Value(1),
                    output_field=models.IntegerField(),
                ),
                "-passed_year",
                "-enrolled_year"
            ),
            "social_media": SocialMedia.objects.filter(is_public=True).order_by("name"),
            "settings": Setting.objects.filter(is_public=True).order_by("type"),
            "seo": SEOPageSetting.objects.filter(is_public=True).order_by("page"),
            "sitemap": SitemapSetting.objects.filter(is_public=True).order_by("priority"),
            "display": DisplaySetting.objects.filter(is_public=True).order_by("context"),
        }