# apps/hires/admin/views.py
from rest_framework import filters
from config.admin.base import AdminBaseViewSet
from ..models import HiringMessage
from ..serializers import HiringMessageSerializer

class AdminHiringMessageViewSet(AdminBaseViewSet):
    """Admin API (CRUD, JWT protected)"""
    serializer_class = HiringMessageSerializer

    def get_queryset(self):
        qs = HiringMessage.objects.all().order_by("-posted_at")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "phone", "details", "ip_address", "user_agent"]
    ordering_fields = ["posted_at", "name", "email"]
    ordering = ["-posted_at"]
