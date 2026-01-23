# apps/auth/token/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Issues JWT tokens and stores them in HttpOnly cookies
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        response.set_cookie(
            key="access",
            value=data["access"],
            httponly=True,
            secure=True,          # True in production
            samesite="Strict",
            max_age=300,          # 5 minutes
        )

        response.set_cookie(
            key="refresh",
            value=data["refresh"],
            httponly=True,
            secure=True,          # True in production
            samesite="Strict",
            max_age=86400,        # 1 day
        )

        # Never return tokens in JSON
        response.data = {"ok": True}
        return response
