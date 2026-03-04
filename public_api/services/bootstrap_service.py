# apps/public_api/services/bootstrap_service.py
from django.db.models import Prefetch

from profiles.models import Profile
from services.models import Service
from skills.models import Skill, SubSkill
from experience.models import Experience
from qualifications.models import Qualification
from socialmedia.models import SocialMedia
from settings.models import (
    Setting,
    SEOPageSetting,
    SitemapSetting,
    DisplaySetting
)

class BootstrapService:

    @staticmethod
    def get_data():

        profile = Profile.objects.first()

        skills = Skill.objects.prefetch_related(
            Prefetch("subskills", queryset=SubSkill.objects.all())
        )
        print("Bootstrap executed")

        return {
            "profile": profile,
            "services": Service.objects.all(),
            "skills": skills,
            "experience": Experience.objects.all(),
            "qualifications": Qualification.objects.all(),
            "social_media": SocialMedia.objects.all(),
            "settings": Setting.objects.all(),
            "seo": SEOPageSetting.objects.all(),
            "sitemap": SitemapSetting.objects.all(),
            "display": DisplaySetting.objects.first(),
        }