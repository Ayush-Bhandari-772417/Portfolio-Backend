# apps/services/admin/views.py
from rest_framework import viewsets, permissions, filters
from ..models import Service
from ..serializers import ServiceSerializer

class AdminServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by("title")
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at", "updated_at"]
    ordering = ["title"]
