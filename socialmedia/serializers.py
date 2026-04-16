# apps/socialmedia/serializers.py
from rest_framework import serializers
from .models import SocialMedia
from config.serializers.base import BaseModelSerializer

class SocialMediaSerializer(BaseModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"
