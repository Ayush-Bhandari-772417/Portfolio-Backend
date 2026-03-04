# apps/public_api/serializers/bootstrap.py
from profiles.serializers import ProfileSerializer
from services.serializers import ServiceSerializer
from skills.serializers import SkillSerializer
from experience.serializers import ExperienceSerializer
from qualifications.serializers import QualificationSerializer
from socialmedia.serializers import SocialMediaSerializer
from settings.serializers import (
    SettingSerializer,
    SEOPageSettingSerializer,
    SitemapSettingSerializer,
    DisplaySettingSerializer
)
from rest_framework import serializers

class BootstrapSerializer(serializers.Serializer):
    profile = ProfileSerializer()
    services = ServiceSerializer(many=True)
    skills = SkillSerializer(many=True)
    experience = ExperienceSerializer(many=True)
    qualifications = QualificationSerializer(many=True)
    social_media = SocialMediaSerializer(many=True)
    settings = SettingSerializer(many=True)
    seo = SEOPageSettingSerializer(many=True)
    sitemap = SitemapSettingSerializer(many=True)
    display = DisplaySettingSerializer()