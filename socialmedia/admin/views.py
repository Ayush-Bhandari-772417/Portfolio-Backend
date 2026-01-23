# apps/socialmedia/admin/views.py
from rest_framework import viewsets, filters, permissions
from ..models import SocialMedia
from ..serializers import SocialMediaSerializer

class AdminSocialMediaViewSet(viewsets.ModelViewSet):
    queryset = SocialMedia.objects.all().order_by("name")
    serializer_class = SocialMediaSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
