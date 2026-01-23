# apps/contacts/admin/views.py
from rest_framework import viewsets, permissions, filters
from ..models import ContactMessage
from ..serializers import ContactMessageSerializer

class AdminContactMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAdminUser]

    queryset = ContactMessage.objects.all().order_by("-created_at")

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "message", "ip_address", "user_agent"]
    ordering_fields = ["created_at", "name", "email"]
    ordering = ["-created_at"]
