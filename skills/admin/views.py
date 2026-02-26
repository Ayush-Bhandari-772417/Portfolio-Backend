# apps/skills/admin/views.py
from rest_framework import viewsets, filters
from config.permissions import IsSecureAdmin
from config.authentication import CookieJWTAuthentication
from ..models import Skill, SubSkill
from ..serializers import SkillSerializer, SubSkillSerializer
from rest_framework.response import Response
from rest_framework import status

class AdminSkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    permission_classes = [IsSecureAdmin]
    authentication_classes = [CookieJWTAuthentication]
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

class AdminSubSkillViewSet(viewsets.ModelViewSet):
    queryset = SubSkill.objects.all().order_by("name")
    serializer_class = SubSkillSerializer
    permission_classes = [IsSecureAdmin]
    authentication_classes = [CookieJWTAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
