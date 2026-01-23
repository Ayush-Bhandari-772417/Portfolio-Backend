# apps/profiles/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.admin.views import AdminProfileViewSet
from profiles.public.views import PublicProfileViewSet

admin_router = DefaultRouter()
admin_router.register("profile", AdminProfileViewSet, basename="admin-profile")

public_router = DefaultRouter()
public_router.register("profile", PublicProfileViewSet, basename="public-profile")

urlpatterns = [
    path("admin/", include(admin_router.urls)),
    path("public/", include(public_router.urls)),
]
