# apps/contacts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contacts.admin.views import AdminContactMessageViewSet
from contacts.public.views import PublicContactMessageViewSet

router_public = DefaultRouter()
router_public.register(r'contacts', PublicContactMessageViewSet, basename='public-contact')

router_admin = DefaultRouter()
router_admin.register(r'contacts', AdminContactMessageViewSet, basename='admin-contact')

urlpatterns = [
    path("public/", include(router_public.urls)),
    path("admin/", include(router_admin.urls)),
]
