# apps/socialmedia/public/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from ..models import SocialMedia
from ..serializers import SocialMediaSerializer

class PublicSocialMediaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SocialMediaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [AllowAny]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        return SocialMedia.objects.filter(is_public=True).order_by("name")
