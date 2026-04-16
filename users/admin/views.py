# apps/users/admin/views.py
from config.admin.base import AdminBaseViewSet
from ..models import User
from ..serializers import UserSerializer


class AdminUserViewSet(AdminBaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
