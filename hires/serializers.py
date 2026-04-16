# apps/hires/serializers.py
from .models import HiringMessage
from config.serializers.base import BaseModelSerializer

class HiringMessageSerializer(BaseModelSerializer):
    class Meta:
        model = HiringMessage
        fields = "__all__"
        read_only_fields = ["posted_at"]
        