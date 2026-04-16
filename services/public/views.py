# apps/services/public/views.py
from rest_framework import filters
from config.public.base import PublicBaseReadOnlyViewSet
from ..models import Service
from ..serializers import ServiceSerializer

class PublicServiceViewSet(PublicBaseReadOnlyViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        qs = Service.objects.filter(is_public=True).order_by("title")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at", "updated_at"]
    ordering = ["title"]
