# apps/auth/token/views.py
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings

@method_decorator(csrf_exempt, name="dispatch")
class CookieTokenObtainPairView(TokenObtainPairView):
    authentication_classes = []      # 🔑 THIS IS THE FIX
    permission_classes = [AllowAny]  # 🔑 REQUIRED

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code != 200:
            return response

        data = response.data
        secure = not settings.DEBUG

        response.set_cookie(
            "access",
            data["access"],
            httponly=True,
            secure=secure,
            samesite="None" if secure else "Lax",
            max_age=300,
        )
        response.set_cookie(
            "refresh",
            data["refresh"],
            httponly=True,
            secure=secure,
            samesite="None" if secure else "Lax",
            max_age=86400,
        )

        response.data = {"ok": True}
        return response
