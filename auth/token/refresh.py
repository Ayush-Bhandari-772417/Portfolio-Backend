# # # # apps/auth/token/refresh.py
# # # from rest_framework_simplejwt.views import TokenRefreshView
# # # from django.conf import settings
# # # from rest_framework.permissions import AllowAny
# # # from rest_framework.response import Response

# # # class CookieTokenRefreshView(TokenRefreshView):
# # #     authentication_classes = []
# # #     permission_classes = [AllowAny]

# # #     def post(self, request, *args, **kwargs):
# # #         refresh = request.COOKIES.get("refresh")
# # #         if not refresh:
# # #             return Response({"detail": "No refresh token"}, status=401)

# # #         data = request.data.copy()
# # #         data["refresh"] = refresh
# # #         request._full_data = data

# # #         response = super().post(request, *args, **kwargs)

# # #         secure = not settings.DEBUG
# # #         response.set_cookie(
            
# # #     "access",
# # #     data["access"],
# # #     httponly=True,
# # #     secure=False,      # not HTTPS
# # #     samesite="None",   # cross-site
# # #     path="/",
# # #     max_age=300,
# # #         )

# # #         response.data = {"ok": True}
# # #         print("Refreshed access token cookie set.")
# # #         return response




# # # apps/auth/token/refresh.py
# # from rest_framework_simplejwt.views import TokenRefreshView
# # from django.conf import settings
# # from rest_framework.permissions import AllowAny
# # from rest_framework.response import Response
# # class CookieTokenRefreshView(TokenRefreshView):
# #     authentication_classes = []
# #     permission_classes = [AllowAny]

# #     def post(self, request, *args, **kwargs):
# #         refresh = request.COOKIES.get("refresh")
# #         if not refresh:
# #             return Response({"detail": "No refresh"}, status=401)

# #         request._full_data = {"refresh": refresh}
# #         response = super().post(request, *args, **kwargs)
# #         secure = not settings.DEBUG
# #         samesite = "None" if not settings.DEBUG else "Lax"
# #         response.set_cookie(
# #             "access",
# #             response.data["access"],
# #             httponly=True,
# #             secure=secure,
# #             samesite=samesite,
# #             path="/",
# #             max_age=300,
# #         )

# #         response.data = {"ok": True}
# #         return response
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken


# class CookieTokenRefreshView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         refresh_token = request.COOKIES.get("refresh")

#         if not refresh_token:
#             return Response(
#                 {"detail": "No refresh token"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         try:
#             refresh = RefreshToken(refresh_token)
#             access = refresh.access_token
#         except Exception:
#             return Response(
#                 {"detail": "Invalid refresh token"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         response = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)

#         response.set_cookie(
#             key="access",
#             value=str(access),
#             httponly=True,
#             secure=settings.AUTH_COOKIE_SECURE,
#             samesite=settings.AUTH_COOKIE_SAMESITE,
#             path="/",
#         )

#         return response









# apps/auth/token/refresh.py
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

class CookieTokenRefreshView(TokenRefreshView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response({"detail": "No refresh"}, status=401)

        request._full_data = {"refresh": refresh}
        response = super().post(request, *args, **kwargs)

        # Update access cookie
        response.set_cookie(
            "access",
            response.data["access"],
            httponly=True,
            secure=settings.AUTH_COOKIE_SECURE,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            path="/",
            max_age=300,
        )

        response.data = {"ok": True}
        return response
