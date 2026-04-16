# apps/skills/public/views.py
from rest_framework import filters
from config.public.base import PublicBaseReadOnlyViewSet
from ..models import Skill, SubSkill
from ..serializers import SkillSerializer, SubSkillSerializer

class PublicSkillViewSet(PublicBaseReadOnlyViewSet):
    """Public-facing API: only fetch visible skills"""
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        return Skill.objects.filter(is_public=True).order_by("name")


class PublicSubSkillViewSet(PublicBaseReadOnlyViewSet):
    """Public-facing API: only fetch visible subskills"""
    serializer_class = SubSkillSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        return SubSkill.objects.filter(is_public=True).order_by("name")
