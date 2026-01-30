# backend/auth/token/urls.py
from django.urls import path
from .refresh import CookieTokenRefreshView
from .views import CookieTokenObtainPairView

urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token-refresh'),
]
