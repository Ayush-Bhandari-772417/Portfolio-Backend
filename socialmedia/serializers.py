# apps/socialmedia/serializers.py
from rest_framework import serializers
from .models import SocialMedia
from core.utils.revalidate import trigger_revalidation

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"

    def create(self, validated_data):
        socialmeedia = super().create(validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return socialmeedia
    
    def update(self, instance, validated_data):
        socialmeedia = super().update(instance, validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return socialmeedia