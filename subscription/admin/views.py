# apps/subscription/admin/views.py
from rest_framework import viewsets, filters
from config.permissions import IsSecureAdmin
from config.authentication import CookieJWTAuthentication
from ..models import Subscription
from ..serializers import SubscriptionSerializer

class AdminSubscriptionViewSet(viewsets.ModelViewSet):
    """Admin API (CRUD, JWT protected)"""
    queryset = Subscription.objects.all().order_by("-subscribed_at")
    serializer_class = SubscriptionSerializer
    permission_classes = [IsSecureAdmin]
    authentication_classes = [CookieJWTAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["email", "ip_address", "user_agent"]
    ordering_fields = ["subscribed_at", "email"]
    ordering = ["-subscribed_at"]
