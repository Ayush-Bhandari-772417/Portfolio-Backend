# apps/settings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from settings.public.views import PublicSettingViewset, PublicSEOPageSettingViwset, PublicSitemapSettingViewset, PublicDisplaySettingViewSet
from settings.admin.views import AdminSettingViewset, AdminSEOPageSettingViwset, AdminSitemapSettingViewset, AdminDisplaySettingViewSet

public_router = DefaultRouter()
public_router.register(r'settings', PublicSettingViewset, basename='settings')
public_router.register(r'seosettings', PublicSEOPageSettingViwset, basename='seosettings')
public_router.register(r'sitemapsettings', PublicSitemapSettingViewset, basename='sitemapsettings')
public_router.register(r'displaysettings', PublicDisplaySettingViewSet, basename='displaysettings')

admin_router = DefaultRouter()
admin_router.register(r'settings', AdminSettingViewset, basename='settings')
admin_router.register(r'seosettings', AdminSEOPageSettingViwset, basename='seosettings')
admin_router.register(r'sitemapsettings', AdminSitemapSettingViewset, basename='sitemapsettings')
admin_router.register(r'displaysettings', AdminDisplaySettingViewSet, basename='displaysettings')

urlpatterns = [
    path('public/', include(public_router.urls)),
    path('admin/', include(admin_router.urls)),
]
