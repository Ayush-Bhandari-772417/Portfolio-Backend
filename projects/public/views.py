# apps/projects/public/views.py
from rest_framework import viewsets, filters, parsers
from django.db import models
from ..models import Project
from ..serializers import ProjectSerializer

class PublicProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Public-facing API (read-only)"""
    queryset = Project.objects.filter(is_public=True).order_by("-started_date")
    serializer_class = ProjectSerializer
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["started_date", "completed_date", "created_at", "posted_at", "title"]
    lookup_field = "slug"

    def get_queryset(self):
        return Project.objects.filter(is_public=True).order_by(
            models.Case(
                models.When(completed_date__isnull=True, then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            "-completed_date",
            "-started_date"
        )
