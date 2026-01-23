# apps/services/serializers.py
from rest_framework import serializers
from .models import Service
from core.utils.revalidate import trigger_revalidation

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

    def create(self, validated_data):
        service = super().create(validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return service
    
    def update(self, instance, validated_data):
        service = super().update(instance, validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return service
