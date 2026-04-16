# apps/services/admin/views.py
from rest_framework import filters
from config.admin.base import AdminBaseViewSet
from ..models import Service
from ..serializers import ServiceSerializer

class AdminServiceViewSet(AdminBaseViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        qs = Service.objects.all().order_by("title")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at", "updated_at"]
    ordering = ["title"]
