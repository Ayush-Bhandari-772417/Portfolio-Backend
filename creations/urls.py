# apps/creations/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from creations.public.views import PublicCategoryViewSet, PublicCreationViewSet
from creations.admin.views import AdminCategoryViewSet, AdminCreationViewSet, ImageUploadView

public_router = DefaultRouter()
public_router.register(r'creations', PublicCreationViewSet, basename='creation')
public_router.register(r'categories', PublicCategoryViewSet, basename='category')

admin_router = DefaultRouter()
admin_router.register(r'creations', AdminCreationViewSet, basename='creation')
admin_router.register(r'categories', AdminCategoryViewSet, basename='category')

urlpatterns = [
    path("public/", include(public_router.urls)),
    path("admin/", include(admin_router.urls)),
    path('admin/upload-image/', ImageUploadView.as_view()),
]
