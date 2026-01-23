# apps/socialmedia/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from socialmedia.admin.views import AdminSocialMediaViewSet
from socialmedia.public.views import PublicSocialMediaViewSet

public_router = DefaultRouter()
public_router.register(r'socialmedias', PublicSocialMediaViewSet, basename='socialmedia')

admin_router = DefaultRouter()
admin_router.register(r'socialmedias', AdminSocialMediaViewSet, basename='socialmedia')

urlpatterns = [
    path("public/", include(public_router.urls)),
    path("admin/", include(admin_router.urls)),
]
