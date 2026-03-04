# apps/public_api/urls.py

from django.urls import path
from .views.bootstrap import BootstrapView

urlpatterns = [
    path("bootstrap/", BootstrapView.as_view(), name="public-bootstrap"),
]