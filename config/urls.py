"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/admin/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/admin/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/admin/auth/', include('auth.token.urls')),
    path('api/admin/auth/me/', include('auth.me.urls')),

    # App APIs (we’ll add routers below)
    path('api/', include('contacts.urls')),
    path('api/', include('creations.urls')),
    path('api/', include('experience.urls')),
    path('api/', include('hires.urls')),
    path('api/', include('profiles.urls')),
    path('api/', include('projects.urls')),
    path('api/', include('qualifications.urls')),
    path('api/', include('services.urls')),
    path('api/', include('settings.urls')),
    path('api/', include('skills.urls')),
    path('api/', include('socialmedia.urls')),
    path('api/', include('subscription.urls')),
    # If you have a separate users app API, include it similarly
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
