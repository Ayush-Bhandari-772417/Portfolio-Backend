# apps/services/public/views.py
from rest_framework import viewsets, filters
from ..models import Service
from ..serializers import ServiceSerializer

class PublicServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(is_public=True).order_by("title")
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at", "updated_at"]
    ordering = ["title"]
