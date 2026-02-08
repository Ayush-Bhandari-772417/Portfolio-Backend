# apps/users/admin/views.py
from rest_framework import viewsets
from config.permissions import IsSecureAdmin
from config.authentication import CookieJWTAuthentication
from ..models import User
from ..serializers import UserSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSecureAdmin]
    authentication_classes = [CookieJWTAuthentication]