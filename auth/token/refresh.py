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
