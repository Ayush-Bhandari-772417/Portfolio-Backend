# apps/settings/admin/views.py
from rest_framework import filters, viewsets
from config.admin.base import AdminBaseViewSet
from ..models import Setting, SEOPageSetting, SitemapSetting, DisplaySetting
from ..serializers import SettingSerializer, SEOPageSettingSerializer, SitemapSettingSerializer, DisplaySettingSerializer

class AdminSettingViewset(AdminBaseViewSet):
    serializer_class = SettingSerializer

    def get_queryset(self):
        qs = Setting.objects.all().order_by("type")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["type"]
    ordering_fields = ["type"]
    ordering = ["type"]


class AdminSEOPageSettingViwset(AdminBaseViewSet):
    serializer_class = SEOPageSettingSerializer

    def get_queryset(self):
        qs = SEOPageSetting.objects.all().order_by("page")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["page"]
    ordering_fields = ["page", "index"]
    ordering = ["page"]
    

class AdminSitemapSettingViewset(AdminBaseViewSet):
    serializer_class = SitemapSettingSerializer

    def get_queryset(self):
        qs = SitemapSetting.objects.all().order_by("priority")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["priority"]
    ordering_fields = ["priority"]
    ordering = ["priority"]


class AdminDisplaySettingViewSet(AdminBaseViewSet):
    serializer_class = DisplaySettingSerializer

    def get_queryset(self):
        qs = DisplaySetting.objects.all().order_by("context")
        return qs

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["context"]
    ordering_fields = ["context"]
    ordering = ["context"]
