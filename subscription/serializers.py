# apps/subscription/serializers.py
from rest_framework import serializers
from .models import Subscription
from config.serializers.base import BaseModelSerializer

class SubscriptionSerializer(BaseModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ["subscribed_at"]
        