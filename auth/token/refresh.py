# apps/auth/token/refresh.py
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings

class CookieTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        # get refresh token from cookie
        request.data["refresh"] = request.COOKIES.get("refresh")
        response = super().post(request, *args, **kwargs)
        data = response.data
        secure = not settings.DEBUG

        # set new access cookie
        response.set_cookie(
            "access",
            data["access"],
            httponly=True,
            secure=secure,
            samesite="None" if secure else "Lax",
            max_age=300,
        )

        response.data = {"ok": True}
        return response
