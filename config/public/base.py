from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination


class PublicPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"


class PublicBaseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Base for public read-only APIs (projects, profiles, skills etc.)
    Enforces:
    - AllowAny perms
    - pagination
    - is_public=True filter
    """
    permission_classes = [AllowAny]
    pagination_class = PublicPagination

    def get_queryset(self):
        qs = super().get_queryset().filter(is_public=True)
        return qs


class PublicBaseCreateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    Base for public write-only APIs (contacts, hires, subscription)
    Enforces:
    - AllowAny perms
    - pagination (for lists if needed)
    """
    permission_classes = [AllowAny]
    pagination_class = PublicPagination

