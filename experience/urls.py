# apps/experience/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from experience.public.views import PublicExperienceViewSet
from experience.admin.views import AdminExperienceViewSet, dashboard_stats

public_router = DefaultRouter()
public_router.register(r'experiences', PublicExperienceViewSet, basename="public-experience")

admin_router = DefaultRouter()
admin_router.register(r'experiences', AdminExperienceViewSet, basename="admin-experience")

urlpatterns = [
    path("public/", include(public_router.urls)),
    path("admin/", include(admin_router.urls)),
    path("admin/dashboard/", dashboard_stats, name="dashboard-stats"),
]
