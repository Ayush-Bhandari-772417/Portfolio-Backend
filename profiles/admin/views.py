# apps/profiles/admin/views.py
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from config.authentication import CookieJWTAuthentication
from config.permissions import IsSecureAdmin
from ..models import Profile
from ..serializers import ProfileSerializer

class AdminProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsSecureAdmin]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    authentication_classes = [CookieJWTAuthentication]

    def get_queryset(self):
        return Profile.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}