# # # # # apps/auth/token/views.py
# # # # from rest_framework.permissions import AllowAny
# # # # from rest_framework.authentication import BasicAuthentication
# # # # from django.views.decorators.csrf import csrf_exempt
# # # # from django.utils.decorators import method_decorator
# # # # from rest_framework_simplejwt.views import TokenObtainPairView
# # # # from django.conf import settings

# # # # @method_decorator(csrf_exempt, name="dispatch")
# # # # class CookieTokenObtainPairView(TokenObtainPairView):
# # # #     authentication_classes = []      # 🔑 THIS IS THE FIX
# # # #     permission_classes = [AllowAny]  # 🔑 REQUIRED

# # # #     def post(self, request, *args, **kwargs):
# # # #         response = super().post(request, *args, **kwargs)

# # # #         if response.status_code != 200:
# # # #             return response

# # # #         data = response.data
# # # #         secure = not settings.DEBUG

# # # #         response.set_cookie(
# # # #             "refresh",
# # # #             data["refresh"],
# # # #             httponly=True,
# # # #             secure=secure,
# # # #             samesite="Lax" if settings.DEBUG else "None",
# # # #             path="/",       # ✅ add this
# # # #             max_age=86400,
# # # #         )

# # # #         response.data = {"ok": True}
# # # #         print("Obtained tokens and set refresh token cookie.")
# # # #         return response





# # # # apps/auth/token/views.py
# # # from rest_framework.permissions import AllowAny
# # # from rest_framework.authentication import BasicAuthentication
# # # from django.views.decorators.csrf import csrf_exempt
# # # from django.utils.decorators import method_decorator
# # # from rest_framework_simplejwt.views import TokenObtainPairView
# # # from django.conf import settings
# # # @method_decorator(csrf_exempt, name="dispatch")
# # # class CookieTokenObtainPairView(TokenObtainPairView):
# # #     authentication_classes = []
# # #     permission_classes = [AllowAny]

# # #     def post(self, request, *args, **kwargs):
# # #         response = super().post(request, *args, **kwargs)

# # #         if response.status_code != 200:
# # #             return response

# # #         data = response.data
# # #         secure = not settings.DEBUG
# # #         samesite = "None" if not settings.DEBUG else "Lax"

# # #         response.set_cookie(
# # #             "refresh",
# # #             data["refresh"],
# # #             httponly=True,
# # #             secure=secure,
# # #             samesite=samesite,
# # #             path="/",
# # #             max_age=86400,
# # #         )

# # #         response.set_cookie(
# # #             "access",
# # #             data["access"],
# # #             httponly=True,
# # #             secure=secure,
# # #             samesite=samesite,
# # #             path="/",
# # #             max_age=300,
# # #         )

# # #         response.data = {"ok": True}
# # #         return response






# # # apps/auth/token/views.py
# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from django.conf import settings
# # from rest_framework.permissions import AllowAny
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from django.contrib.auth import authenticate

# # class CookieTokenObtainPairView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         username = request.data.get("username")
# #         password = request.data.get("password")

# #         user = authenticate(username=username, password=password)

# #         if not user or not user.is_staff:
# #             return Response(
# #                 {"detail": "Invalid credentials"},
# #                 status=status.HTTP_401_UNAUTHORIZED,
# #             )

# #         refresh = RefreshToken.for_user(user)

# #         response = Response(
# #             {"detail": "Login successful"},
# #             status=status.HTTP_200_OK,
# #         )

# #         # ACCESS TOKEN COOKIE (path=/ so it’s sent to all endpoints)
# #         response.set_cookie(
# #             key="access",
# #             value=str(refresh.access_token),
# #             httponly=True,
# #             secure=settings.AUTH_COOKIE_SECURE,
# #             samesite=settings.AUTH_COOKIE_SAMESITE,
# #             path="/",
# #             max_age=300,  # 5 minutes
# #         )

# #         # REFRESH TOKEN COOKIE
# #         response.set_cookie(
# #             key="refresh",
# #             value=str(refresh),
# #             httponly=True,
# #             secure=settings.AUTH_COOKIE_SECURE,
# #             samesite=settings.AUTH_COOKIE_SAMESITE,
# #             path="/",
# #             max_age=12*60*60,  # 12 hours
# #         )

# #         return response






# # apps/auth/token/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator


# @method_decorator(csrf_exempt, name="dispatch")
# class CookieTokenObtainPairView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(username=username, password=password)

#         if not user or not user.is_staff:
#             return Response(
#                 {"detail": "Invalid credentials"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         refresh = RefreshToken.for_user(user)

#         response = Response(
#             {"detail": "Login successful"},
#             status=status.HTTP_200_OK,
#         )

#         response.set_cookie(
#             key="access",
#             value=str(refresh.access_token),
#             httponly=True,
#             secure=settings.AUTH_COOKIE_SECURE,
#             samesite=settings.AUTH_COOKIE_SAMESITE,
#             path="/",
#         )

#         response.set_cookie(
#             key="refresh",
#             value=str(refresh),
#             httponly=True,
#             secure=settings.AUTH_COOKIE_SECURE,
#             samesite=settings.AUTH_COOKIE_SAMESITE,
#             path="/",
#         )

#         print("Setting cookies in response")
#         return response





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