# apps/hires/serializers.py
from rest_framework import serializers
from .models import HiringMessage

class HiringMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringMessage
        fields = "__all__"
        read_only_fields = ["posted_at"]
        