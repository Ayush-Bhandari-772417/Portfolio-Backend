# apps/qualifications/admin/views.py
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.db import models
from ..models import Qualification
from ..serializers import QualificationSerializer

class AdminQualificationViewSet(viewsets.ModelViewSet):
    """Admin API (CRUD, JWT protected) with search + ordering"""
    serializer_class = QualificationSerializer
    permission_classes = [permissions.IsAdminUser]

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["board_name", "school_name", "location", "description"]
    ordering_fields = ["enrolled_year", "passed_year", "board_name", "school_name"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("\n\n⛔ PROJECT CREATE ERROR:")
            print(serializer.errors)
            print("\nRequest Data:", request.data)
            return Response(serializer.errors, status=400)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            print("\n\n⛔ PROJECT UPDATE ERROR:")
            print(serializer.errors)
            print("\nRequest Data:", request.data)
            return Response(serializer.errors, status=400)

        serializer.save()
        return Response(serializer.data)


    def get_queryset(self):
        # Ongoing first, then completed
        return Qualification.objects.all().order_by(
            models.Case(
                models.When(passed_year__isnull=True, then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            "-passed_year",
            "-enrolled_year"
        )
