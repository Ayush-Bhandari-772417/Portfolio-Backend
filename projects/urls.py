# apps/projects/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from projects.public.views import PublicProjectViewSet
from projects.admin.views import AdminProjectViewSet

public_router = DefaultRouter()
public_router.register(r'projects', PublicProjectViewSet, basename='project')

admin_router = DefaultRouter()
admin_router.register(r'projects', AdminProjectViewSet, basename='project')

urlpatterns = [
    path("public/", include(public_router.urls)),
    path("admin/", include(admin_router.urls)),
]
