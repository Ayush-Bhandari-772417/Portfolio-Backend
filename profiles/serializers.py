# apps/profiles/serializers.py
from rest_framework import serializers
from .models import Profile
from core.utils.revalidate import trigger_revalidation

# Main Project Serializer
class ProfileSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    about_image_url = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()
    named_logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def validate_resume(self, value):
        if value and not value.name.endswith(".pdf"):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value

    def get_resume_url(self, obj):
        request = self.context.get("request")
        if obj.resume and hasattr(obj.resume, "url"):
            return request.build_absolute_uri(obj.resume.url) if request else obj.resume.url
        return None

    def get_profile_image_url(self, obj):
        request = self.context.get("request")
        if obj.profile_image and hasattr(obj.profile_image, "url"):
            return request.build_absolute_uri(obj.profile_image.url) if request else obj.profile_image.url
        return None

    def get_about_image_url(self, obj):
        request = self.context.get("request")
        if obj.about_image and hasattr(obj.about_image, "url"):
            return request.build_absolute_uri(obj.about_image.url) if request else obj.about_image.url
        return None

    def get_logo_url(self, obj):
        request = self.context.get("request")
        if obj.logo and hasattr(obj.logo, "url"):
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None

    def get_named_logo_url(self, obj):
        request = self.context.get("request")
        if obj.named_logo and hasattr(obj.named_logo, "url"):
            return request.build_absolute_uri(obj.named_logo.url) if request else obj.named_logo.url
        return None

    def create(self, validated_data):
        profile = super().create(validated_data)
        trigger_revalidation(paths=[ "/", ])
        return profile

    def update(self, instance, validated_data):
        profile = super().update(instance, validated_data)
        trigger_revalidation(paths=[ "/", ])
        return profile

    def validate(self, data):
        if Profile.objects.exists() and not self.instance:
            raise serializers.ValidationError("Only one profile allowed.")
        return data
