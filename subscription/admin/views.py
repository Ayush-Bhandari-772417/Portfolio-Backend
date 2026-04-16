# apps/subscription/admin/views.py
from rest_framework import filters
from config.admin.base import AdminBaseViewSet
from ..models import Subscription
from ..serializers import SubscriptionSerializer

class AdminSubscriptionViewSet(AdminBaseViewSet):
    """Admin API (CRUD, JWT protected)"""
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        qs = Subscription.objects.all().order_by("-subscribed_at")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["email", "ip_address", "user_agent"]
    ordering_fields = ["subscribed_at", "email"]
    ordering = ["-subscribed_at"]
