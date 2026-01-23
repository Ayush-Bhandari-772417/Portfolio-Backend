# apps/services/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from services.public.views import PublicServiceViewSet
from services.admin.views import AdminServiceViewSet

public_router = DefaultRouter()
public_router.register(r'services', PublicServiceViewSet, basename='service')

admin_router = DefaultRouter()
admin_router.register(r'services', AdminServiceViewSet, basename='service')

urlpatterns = [
    path("public/", include(public_router.urls)),
    path("admin/", include(admin_router.urls)),
]
