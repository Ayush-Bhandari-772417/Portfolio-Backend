# apps/socialmedia/admin/views.py
from rest_framework import filters
from config.admin.base import AdminBaseViewSet
from ..models import SocialMedia
from ..serializers import SocialMediaSerializer

class AdminSocialMediaViewSet(AdminBaseViewSet):
    serializer_class = SocialMediaSerializer

    def get_queryset(self):
        qs = SocialMedia.objects.all().order_by("name")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

