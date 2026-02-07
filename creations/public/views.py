# apps/creations/public/views.py

from rest_framework import viewsets, filters, parsers
from django.db import models
from rest_framework.permissions import AllowAny
from ..models import Creation, Category
from ..serializers import CreationSerializer, CategorySerializer


class PublicCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_public=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class PublicCreationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Creation.objects.filter(is_public=True)
    serializer_class = CreationSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    search_fields = ["title", "excerpt", "keywords"]
    ordering_fields = ["published_date", "written_date", "title"]

    def get_queryset(self):
        queryset = Creation.objects.filter(is_public=True).select_related("category")

        # filter by ?type=blog
        type_param = self.request.query_params.get("type")
        if type_param:
            queryset = queryset.filter(type=type_param)

        # ordering (drafts last)
        return queryset.order_by(
            models.Case(
                models.When(published_date__isnull=True, then=1),
                default=0,
                output_field=models.IntegerField(),
            ),
            "-published_date",
            "-written_date"
        )
