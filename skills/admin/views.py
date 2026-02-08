# apps/skills/admin/views.py
from rest_framework import viewsets, filters, permissions
from config.permissions import IsSecureAdmin
from config.authentication import CookieJWTAuthentication
from ..models import Skill, SubSkill
from ..serializers import SkillSerializer, SubSkillSerializer

class AdminSkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    permission_classes = [IsSecureAdmin]
    authentication_classes = [CookieJWTAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class AdminSubSkillViewSet(viewsets.ModelViewSet):
    queryset = SubSkill.objects.all().order_by("name")
    serializer_class = SubSkillSerializer
    permission_classes = [IsSecureAdmin]
    authentication_classes = [CookieJWTAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
