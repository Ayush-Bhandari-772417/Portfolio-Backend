# backend/auth/token/urls.py
from django.urls import path
from .views import CookieTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
