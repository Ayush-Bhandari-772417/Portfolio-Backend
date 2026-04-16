# apps/creations/public/views.py

from rest_framework import filters, parsers
from django.db import models
from config.public.base import PublicBaseReadOnlyViewSet
from ..models import Creation, Category
from ..serializers import CreationSerializer, CategorySerializer, CreationListSerializer, CreationDetailSerializer


class PublicCategoryViewSet(PublicBaseReadOnlyViewSet):
    serializer_class = CategorySerializer


class PublicCreationViewSet(PublicBaseReadOnlyViewSet):
    serializer_class = CreationSerializer
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
    
    def get_serializer_class(self):
        if self.action == "list":
            return CreationListSerializer
        return CreationDetailSerializer