# # backend/config/permissions.py
# from rest_framework.permissions import BasePermission
# from django.conf import settings
# from .security import is_allowed_admin_ip


# class IsSecureAdmin(BasePermission):

#     def has_permission(self, request, view):

#         user = request.user

#         # Must be authenticated
#         if not user or not user.is_authenticated:
#             return False

#         # Must be staff
#         if not user.is_staff:
#             return False

#         # In production → check IP
#         if not settings.DEBUG:
#             if not is_allowed_admin_ip(request):
#                 return False

#         return True




# backend/config/permissions.py
from rest_framework.permissions import BasePermission
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from .security import is_allowed_admin_ip


class IsSecureAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if not user.is_staff:
            return False

        if not settings.DEBUG:
            if not is_allowed_admin_ip(request):
                raise PermissionDenied("Admin access not allowed from this IP")

        return True
