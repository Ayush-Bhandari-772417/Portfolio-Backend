# apps/experience/public/views.py
from rest_framework import viewsets, filters
from django.db import models
from rest_framework.permissions import AllowAny
from ..models import Experience
from ..serializers import ExperienceSerializer

class PublicExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """Public-facing API (read-only, search + ordering enabled)"""

    serializer_class = ExperienceSerializer
    permission_classes = [AllowAny]

    # Search + filtering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # Allow searching
    search_fields = [ "title", "organization", "location", "responsibilities", ]

    # Allow ordering
    ordering_fields = [ "start_date", "end_date", "title", "organization", "location", ]

    # Default frontend ordering
    ordering = ["-start_date"]

    def get_queryset(self):
        """Show only public experiences, ongoing first."""
        return Experience.objects.filter(is_public=True).order_by(
            models.Case(
                models.When(end_date__isnull=True, then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            "-start_date",
        )

