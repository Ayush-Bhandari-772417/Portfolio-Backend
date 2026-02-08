# apps/contacts/admin/views.py
from rest_framework import viewsets, filters
from config.permissions import IsSecureAdmin
from ..models import ContactMessage
from ..serializers import ContactMessageSerializer
from config.authentication import CookieJWTAuthentication

class AdminContactMessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = ContactMessageSerializer
    permission_classes = [IsSecureAdmin]

    queryset = ContactMessage.objects.all().order_by("-created_at")

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "message", "ip_address", "user_agent"]
    ordering_fields = ["created_at", "name", "email"]
    ordering = ["-created_at"]
