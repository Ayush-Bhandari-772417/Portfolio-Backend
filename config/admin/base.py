from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination


class AdminPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"


class AdminBaseViewSet(viewsets.ModelViewSet):
    """
    All admin APIs MUST inherit this.
    Enforces:
    - pagination
    - ordering consistency
    - future audit hooks
    """

    pagination_class = AdminPagination

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("-id")

