# apps/qualifications/serializers.py
from rest_framework import serializers
from .models import Qualification
from core.utils.revalidate import trigger_revalidation

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = "__all__"

    def create(self, validated_data):
        qualification = super().create(validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return qualification
    
    def update(self, instance, validated_data):
        qualification = super().update(instance, validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return qualification
