# apps/creations/admin/views.py

from django.core.files.storage import default_storage
from django.conf import settings
import uuid
from django.db import models
from rest_framework import viewsets, filters, parsers
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from config.permissions import IsSecureAdmin
from django.shortcuts import get_object_or_404
from core.utils.revalidate import trigger_revalidation

from ..models import Creation, Category
from ..serializers import CreationSerializer, CategorySerializer

from config.authentication import CookieJWTAuthentication

class AdminCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [CookieJWTAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSecureAdmin]


class AdminCreationViewSet(viewsets.ModelViewSet):
    authentication_classes = [CookieJWTAuthentication]
    queryset = Creation.objects.all().select_related("category")
    serializer_class = CreationSerializer
    permission_classes = [IsSecureAdmin]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    search_fields = ["title", "excerpt", "keywords"]
    ordering_fields = ["published_date", "written_date", "title"]

    lookup_field = "slug"  # default slug for detail URLs

    def get_object(self):
        lookup = self.kwargs.get(self.lookup_field)

        # allow numeric ID or slug
        if lookup.isdigit():
            return get_object_or_404(Creation, pk=int(lookup))
        return get_object_or_404(Creation, slug=lookup)

    def get_queryset(self):
        queryset = Creation.objects.all().prefetch_related( "category")
        type_param = self.request.query_params.get("type")
        if type_param:
            queryset = queryset.filter(type=type_param)
        return queryset.order_by(
            models.Case(
                models.When(published_date__isnull=True, then=1),
                default=0,
                output_field=models.IntegerField(),
            ),
            "-published_date",
            "-written_date"
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        slug = instance.slug
        category = instance.category.id if instance.category else None
        response = super().destroy(request, *args, **kwargs)
        paths = ["/creations"]
        if category:
            paths.append(f"/creations/{category}")
        paths.append(f"/creations/{slug}")
        trigger_revalidation(paths=paths)
        return response


class ImageUploadView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    parser_classes = [MultiPartParser]
    permission_classes = [IsSecureAdmin]

    def post(self, request):
        file = request.FILES.get("image")
        if not file:
            return Response({"error": "No image"}, status=400)

        filename = f"editor/{uuid.uuid4()}_{file.name}"
        path = default_storage.save(filename, file)

        # 🔑 IMPORTANT PART
        url = request.build_absolute_uri(settings.MEDIA_URL + path)

        return Response({"url": url})
