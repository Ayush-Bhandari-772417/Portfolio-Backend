# apps/auth/token/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class CookieTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        print(f"[LOGIN ATTEMPT] username={username}, password provided={bool(password)}")

        user = authenticate(username=username, password=password)

        if not user:
            print("[LOGIN] Authentication failed")
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_staff:
            print(f"[LOGIN] User {username} is not staff")
            return Response(
                {"detail": "User is not staff"},
                status=status.HTTP_403_FORBIDDEN,   # ← better to return 403 here
            )

        print(f"[LOGIN SUCCESS] User {username} authenticated, is_staff={user.is_staff}")

        refresh = RefreshToken.for_user(user)

        response = Response(
            {"detail": "Login successful"},
            status=status.HTTP_200_OK,
        )

        print("[LOGIN] Setting access cookie")
        response.set_cookie(
            key="access",
            value=str(refresh.access_token),
            httponly=True,
            secure=settings.AUTH_COOKIE_SECURE,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            path="/",
        )

        print("[LOGIN] Setting refresh cookie")
        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=settings.AUTH_COOKIE_SECURE,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            path="/",
        )

        print("[LOGIN] Cookies should be set now")
        return response