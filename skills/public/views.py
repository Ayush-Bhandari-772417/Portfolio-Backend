# apps/skills/public/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from ..models import Skill, SubSkill
from ..serializers import SkillSerializer, SubSkillSerializer

class PublicSkillViewSet(viewsets.ReadOnlyModelViewSet):
    """Public-facing API: only fetch visible skills"""
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        return Skill.objects.filter(is_public=True).order_by("name")


class PublicSubSkillViewSet(viewsets.ReadOnlyModelViewSet):
    """Public-facing API: only fetch visible subskills"""
    serializer_class = SubSkillSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        return SubSkill.objects.filter(is_public=True).order_by("name")
