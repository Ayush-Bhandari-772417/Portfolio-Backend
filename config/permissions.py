# # # backend/config/permissions.py
# # from rest_framework.permissions import BasePermission
# # from .security import is_allowed_admin_ip

# # class IsSecureAdmin(BasePermission):
# #     def has_permission(self, request, view):
# #         user = request.user

# #         if not user.is_authenticated:
# #             return False

# #         if not user.is_staff:
# #             return False

# #         if not is_allowed_admin_ip(request):
# #             return False

# #         return True


# # backend/config/permissions.py
# from rest_framework.permissions import BasePermission
# from .security import is_allowed_admin_ip
# from django.conf import settings

# class IsSecureAdmin(BasePermission):

#     def has_permission(self, request, view):

#         # Allow everything in DEBUG
#         if settings.DEBUG:
#             return True

#         user = request.user

#         if not user.is_authenticated:
#             return False

#         if not user.is_staff:
#             return False

#         if not is_allowed_admin_ip(request):
#             return False

#         return True





from rest_framework.permissions import BasePermission
from django.conf import settings
from .security import is_allowed_admin_ip


class IsSecureAdmin(BasePermission):

    def has_permission(self, request, view):

        # ✅ Disable IP protection in development
        if settings.DEBUG:
            return True

        user = request.user

        if not user.is_authenticated:
            return False

        if not user.is_staff:
            return False

        if not is_allowed_admin_ip(request):
            return False

        return True
