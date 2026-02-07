# apps/profiles/public/views.py
from rest_framework import viewsets, filters, parsers
from django.db import models
from rest_framework.permissions import AllowAny
from ..models import Profile
from ..serializers import ProfileSerializer

class PublicProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """Public-facing API (read-only)"""
    queryset = Profile.objects.filter(is_public=True)
    serializer_class = ProfileSerializer
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    permission_classes = [AllowAny]