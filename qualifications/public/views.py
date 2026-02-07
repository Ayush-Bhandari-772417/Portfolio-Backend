# apps/qualifications/public/views.py
from rest_framework import viewsets, filters
from django.db import models
from rest_framework.permissions import AllowAny
from ..models import Qualification
from ..serializers import QualificationSerializer

class PublicQualificationViewSet(viewsets.ReadOnlyModelViewSet):
    """Public-facing API (read-only, search + ordering enabled)"""
    serializer_class = QualificationSerializer
    permission_classes = [AllowAny]

    # Enable search + filtering for frontend
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # Fields user should be allowed to search
    search_fields = [ "board_name", "school_name", "location", "description", "grade" ]

    # Fields user should be allowed to order by
    ordering_fields = [ "enrolled_year", "passed_year", "board_name", "school_name", "location", ]

    # Default ordering
    ordering = ["-passed_year"]

    def get_queryset(self):
        # Only show public qualifications, and sort ongoing first
        return Qualification.objects.filter(is_public=True).order_by(
            models.Case(
                models.When(passed_year__isnull=True, then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            "-passed_year",
            "-enrolled_year"
        )
