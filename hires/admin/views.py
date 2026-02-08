# apps/hires/admin/views.py
from rest_framework import viewsets, filters
from config.authentication import CookieJWTAuthentication
from config.permissions import IsSecureAdmin
from ..models import HiringMessage
from ..serializers import HiringMessageSerializer

class AdminHiringMessageViewSet(viewsets.ModelViewSet):
    """Admin API (CRUD, JWT protected)"""
    queryset = HiringMessage.objects.all().order_by("-posted_at")
    serializer_class = HiringMessageSerializer
    permission_classes = [IsSecureAdmin]
    authentication_classes = [CookieJWTAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "phone", "details", "ip_address", "user_agent"]
    ordering_fields = ["posted_at", "name", "email"]
    ordering = ["-posted_at"]
