# apps/skills/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from skills.public.views import PublicSkillViewSet, PublicSubSkillViewSet
from skills.admin.views import AdminSkillViewSet, AdminSubSkillViewSet

public_router = DefaultRouter()
public_router.register(r'skills', PublicSkillViewSet, basename='skill')
public_router.register(r'subskills', PublicSubSkillViewSet, basename='subskill')

admin_router = DefaultRouter()
admin_router.register(r'skills', AdminSkillViewSet, basename='skill')
admin_router.register(r'subskills', AdminSubSkillViewSet, basename='subskill')

urlpatterns = [
    path('public/', include(public_router.urls)),
    path('admin/', include(admin_router.urls)),
]
