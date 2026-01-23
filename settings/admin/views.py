# apps/settings/admin/views.py
from rest_framework import viewsets, filters, permissions
from ..models import Setting, SEOPageSetting, SitemapSetting, DisplaySetting
from ..serializers import SettingSerializer, SEOPageSettingSerializer, SitemapSettingSerializer, DisplaySettingSerializer

class AdminSettingViewset(viewsets.ModelViewSet):
    serializer_class = SettingSerializer
    queryset = Setting.objects.all().order_by("type")
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["type"]
    ordering_fields = ["type"]
    ordering = ["type"]


class AdminSEOPageSettingViwset(viewsets.ModelViewSet):
    serializer_class = SEOPageSettingSerializer
    queryset = SEOPageSetting.objects.all().order_by("page")
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["page"]
    ordering_fields = ["page", "index"]
    ordering = ["page"]
    

class AdminSitemapSettingViewset(viewsets.ModelViewSet):
    serializer_class = SitemapSettingSerializer
    queryset = SitemapSetting.objects.all().order_by("priority")
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["priority"]
    ordering_fields = ["priority"]
    ordering = ["priority"]


class AdminDisplaySettingViewSet(viewsets.ModelViewSet):
    serializer_class = DisplaySettingSerializer
    queryset = DisplaySetting.objects.all().order_by("context")
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["context"]
    ordering_fields = ["context"]
    ordering = ["context"]
