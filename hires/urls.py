# apps/hires/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hires.public.views import PublicHiringMessageViewSet
from hires.admin.views import AdminHiringMessageViewSet

public_router = DefaultRouter()
public_router.register(r'hires', PublicHiringMessageViewSet, basename='hire')

admin_router = DefaultRouter()
admin_router.register(r'hires', AdminHiringMessageViewSet, basename='hire')

urlpatterns = [
    path("public/", include(public_router.urls)),  # ⚠️ no extra /api here
    path("admin/", include(admin_router.urls)),    # ⚠️ no extra /api here
]