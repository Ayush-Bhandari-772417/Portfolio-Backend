# apps/contacts/serializers.py
from .models import ContactMessage
from config.serializers.base import BaseModelSerializer

class ContactMessageSerializer(BaseModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["created_at"]
