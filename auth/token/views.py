# # # # apps/auth/token/views.py
# # # from rest_framework_simplejwt.views import TokenObtainPairView
# # # from django.conf import settings


# # # class CookieTokenObtainPairView(TokenObtainPairView):

# # #     def post(self, request, *args, **kwargs):
# # #         response = super().post(request, *args, **kwargs)
# # #         data = response.data
# # #         secure = not settings.DEBUG
# # #         response.set_cookie(
# # #             key="access",
# # #             value=data["access"],
# # #             httponly=True,
# # #             secure=secure,
# # #             samesite="Lax",
# # #             max_age=300,
# # #         )
# # #         response.set_cookie(
# # #             key="refresh",
# # #             value=data["refresh"],
# # #             httponly=True,
# # #             secure=secure,
# # #             samesite="Lax",
# # #             max_age=86400,
# # #         )
# # #         response.data = {"ok": True}
# # #         return response

# # # apps/auth/token/views.py
# # from urllib import response
# # from rest_framework_simplejwt.views import TokenObtainPairView
# # from django.conf import settings


# # class CookieTokenObtainPairView(TokenObtainPairView):

# #     def post(self, request, *args, **kwargs):
# #         secure = not settings.DEBUG

# #         response.set_cookie(
# #             "access",
# #             data["access"],
# #             httponly=True,
# #             secure=secure,
# #             samesite="None" if secure else "Lax",
# #             max_age=300,
# #         )
# #         response.set_cookie(
# #             "refresh",
# #             data["refresh"],
# #             httponly=True,
# #             secure=secure,
# #             samesite="None" if secure else "Lax",
# #             max_age=86400,
# #         )
# #         return response


# # apps/auth/token/views.py
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.response import Response
# from django.conf import settings

# class CookieTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         # Call parent to authenticate
#         response = super().post(request, *args, **kwargs)

#         # If authentication failed, return parent response
#         if response.status_code != 200:
#             return response

#         data = response.data
#         secure = not settings.DEBUG

#         # Set cookies
#         response.set_cookie(
#             "access", data["access"], httponly=True, secure=secure, samesite="None" if secure else "Lax", max_age=300
#         )
#         response.set_cookie(
#             "refresh", data["refresh"], httponly=True, secure=secure, samesite="None" if secure else "Lax", max_age=86400
#         )

#         response.data = {"ok": True}  # hide tokens in body
#         return response



from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings

@method_decorator(csrf_exempt, name="dispatch")
class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]   # 🔑 REQUIRED

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code != 200:
            return response

        data = response.data
        secure = not settings.DEBUG

        response.set_cookie(
            "access", data["access"],
            httponly=True, secure=secure,
            samesite="None" if secure else "Lax",
            max_age=300,
        )
        response.set_cookie(
            "refresh", data["refresh"],
            httponly=True, secure=secure,
            samesite="None" if secure else "Lax",
            max_age=86400,
        )

        response.data = {"ok": True}
        return response
