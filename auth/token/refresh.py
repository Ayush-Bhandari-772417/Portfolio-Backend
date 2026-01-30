# # apps/auth/token/refresh.py
# from rest_framework_simplejwt.views import TokenRefreshView
# from django.conf import settings

# class CookieTokenRefreshView(TokenRefreshView):

#     def post(self, request, *args, **kwargs):
#         # get refresh token from cookie
#         request.data["refresh"] = request.COOKIES.get("refresh")
#         response = super().post(request, *args, **kwargs)
#         data = response.data
#         secure = not settings.DEBUG

#         # set new access cookie
#         response.set_cookie(
#             "access",
#             data["access"],
#             httponly=True,
#             secure=secure,
#             samesite="None" if secure else "Lax",
#             max_age=300,
#         )

#         response.data = {"ok": True}
#         return response





from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class CookieTokenRefreshView(TokenRefreshView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response({"detail": "No refresh token"}, status=401)

        data = request.data.copy()
        data["refresh"] = refresh
        request._full_data = data

        response = super().post(request, *args, **kwargs)

        secure = not settings.DEBUG
        response.set_cookie(
            "access",
            response.data["access"],
            httponly=True,
            secure=secure,
            samesite="None" if secure else "Lax",
            max_age=300,
        )

        response.data = {"ok": True}
        return response
