# apps/services/serializers.py
from rest_framework import serializers
from .models import Service
from config.serializers.base import BaseModelSerializer

class ServiceSerializer(BaseModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
