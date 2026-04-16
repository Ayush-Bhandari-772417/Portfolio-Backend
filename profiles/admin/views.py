# apps/profiles/admin/views.py
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from config.admin.base import AdminBaseViewSet
from ..models import Profile
from ..serializers import ProfileSerializer

class AdminProfileViewSet(AdminBaseViewSet):
    serializer_class = ProfileSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_queryset(self):
        return Profile.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}