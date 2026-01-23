# apps/experience/serializers.py
from rest_framework import serializers
from .models import Experience
from core.utils.revalidate import trigger_revalidation

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

    def create(self, validated_data):
        experience = super().create(validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return experience
    
    def update(self, instance, validated_data):
        experience = super().update(instance, validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return experience
