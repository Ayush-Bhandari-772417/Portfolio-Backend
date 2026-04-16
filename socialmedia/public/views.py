# apps/socialmedia/public/views.py
from rest_framework import filters
from config.public.base import PublicBaseReadOnlyViewSet
from ..models import SocialMedia
from ..serializers import SocialMediaSerializer

class PublicSocialMediaViewSet(PublicBaseReadOnlyViewSet):
    serializer_class = SocialMediaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_queryset(self):
        return SocialMedia.objects.filter(is_public=True).order_by("name")
