
from rest_framework import serializers
from django.conf import settings

class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for all models. Auto-excludes audit fields, provides standard create/update/validate,
    and image URL helpers.
    """
    # Common audit fields from models
    AUDIT_FIELDS = [
        'created_at', 'updated_at', 'posted_at', 'subscribed_at',
        'uploaded_ip', 'uploaded_by', 'ip_address'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically make audit fields read-only if present
        for field in self.AUDIT_FIELDS:
            if hasattr(self, field) and field in self.fields:
                self.fields[field].read_only = True

    def get_image_url(self, obj, field_name):
        """Shared method for ImageField/FileField absolute URLs."""
        request = self.context.get('request')
        field = getattr(obj, field_name, None)
        if field and hasattr(field, 'url'):
            return request.build_absolute_uri(field.url) if request else field.url
        return None

    def create(self, validated_data):
        """Standard create - override for custom logic."""
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Standard update - override for custom logic."""
        return super().update(instance, validated_data)

    def validate(self, data):
        """Base validation - add app-specific."""
        return data


class BaseNestedSerializer(BaseModelSerializer):
    """For nested many=True serializers like galleries/subskills."""
    pass

