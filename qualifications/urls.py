# apps/qualifications/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from qualifications.public.views import PublicQualificationViewSet
from qualifications.admin.views import AdminQualificationViewSet

public_router = DefaultRouter()
public_router.register(r'qualifications', PublicQualificationViewSet, basename='qualification')

admin_router = DefaultRouter()
admin_router.register(r'qualifications', AdminQualificationViewSet, basename='qualification')

urlpatterns = [
    path("public/", include(public_router.urls)),
    path("admin/", include(admin_router.urls)),
]
