# apps/profiles/serializers.py
from rest_framework import serializers
from config.serializers.base import BaseModelSerializer
from .models import Profile

# Main Project Serializer
class ProfileSerializer(BaseModelSerializer):
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
        return self.get_image_url(obj, 'resume')

    def get_profile_image_url(self, obj):
        return self.get_image_url(obj, 'profile_image')

    def get_about_image_url(self, obj):
        return self.get_image_url(obj, 'about_image')

    def get_logo_url(self, obj):
        return self.get_image_url(obj, 'logo')

    def get_named_logo_url(self, obj):
        return self.get_image_url(obj, 'named_logo')

    def validate(self, data):
        if Profile.objects.exists() and not self.instance:
            raise serializers.ValidationError("Only one profile allowed.")
        return data
