# apps/skills/admin/views.py
from rest_framework import filters
from config.admin.base import AdminBaseViewSet
from ..models import Skill, SubSkill
from ..serializers import SkillSerializer, SubSkillSerializer
from rest_framework.response import Response
from rest_framework import status

class AdminSkillViewSet(AdminBaseViewSet):
    serializer_class = SkillSerializer

    def get_queryset(self):
        qs = Skill.objects.all().order_by("name")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
    
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AdminSubSkillViewSet(AdminBaseViewSet):
    serializer_class = SubSkillSerializer

    def get_queryset(self):
        qs = SubSkill.objects.all().order_by("name")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
