# apps/profiles/public/views.py
from rest_framework import filters, parsers
from django.db import models
from config.public.base import PublicBaseReadOnlyViewSet
from ..models import Profile
from ..serializers import ProfileSerializer

class PublicProfileViewSet(PublicBaseReadOnlyViewSet):
    """Public-facing API (read-only)"""
    serializer_class = ProfileSerializer
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
