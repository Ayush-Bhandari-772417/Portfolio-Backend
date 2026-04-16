# apps/contacts/admin/views.py
from rest_framework import filters
from config.admin.base import AdminBaseViewSet
from ..models import ContactMessage
from ..serializers import ContactMessageSerializer


class AdminContactMessageViewSet(AdminBaseViewSet):
    serializer_class = ContactMessageSerializer

    def get_queryset(self):
        qs = ContactMessage.objects.all().order_by("-created_at")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "message", "ip_address", "user_agent"]
    ordering_fields = ["created_at", "name", "email"]
    ordering = ["-created_at"]
