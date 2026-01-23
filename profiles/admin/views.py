# apps/profiles/admin/views.py
from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from ..models import Profile
from ..serializers import ProfileSerializer

class AdminProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_queryset(self):
        return Profile.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}