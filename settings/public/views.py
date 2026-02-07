# apps/settings/public/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from ..models import Setting, SEOPageSetting, SitemapSetting, DisplaySetting
from ..serializers import SettingSerializer, SEOPageSettingSerializer, SitemapSettingSerializer, DisplaySettingSerializer

class PublicSettingViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = SettingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [AllowAny]
    search_fields = ["type"]
    ordering_fields = ["type"]
    ordering = ["type"]

    def get_queryset(self):
        return Setting.objects.filter(is_public=True).order_by("type")
    

class PublicSEOPageSettingViwset(viewsets.ReadOnlyModelViewSet):
    serializer_class = SEOPageSettingSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["page"]
    ordering_fields = ["page", "index"]
    ordering = ["page"]

    def get_queryset(self):
        return SEOPageSetting.objects.filter(is_public=True).order_by("page")
    

class PublicSitemapSettingViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = SitemapSettingSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["priority"]
    ordering_fields = ["priority"]
    ordering = ["priority"]

    def get_queryset(self):
        return SitemapSetting.objects.filter(is_public=True).order_by("priority")
    

class PublicDisplaySettingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DisplaySettingSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["context"]
    ordering_fields = ["context"]
    ordering = ["context"]

    def get_queryset(self):
        return DisplaySetting.objects.filter(is_public=True).order_by("context")
