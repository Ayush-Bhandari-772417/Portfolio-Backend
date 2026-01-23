# apps/subscription/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from subscription.public.views import PublicSubscriptionViewSet
from subscription.admin.views import AdminSubscriptionViewSet

public_router = DefaultRouter()
public_router.register(r'subscribes', PublicSubscriptionViewSet, basename="public-subscribe")

admin_router = DefaultRouter()
admin_router.register(r'subscribes', AdminSubscriptionViewSet, basename="admin-subscribe")

urlpatterns = [
    path("public/", include(public_router.urls)),  # ⚠️ no extra /api here
    path("admin/", include(admin_router.urls)),    # ⚠️ no extra /api here
]
