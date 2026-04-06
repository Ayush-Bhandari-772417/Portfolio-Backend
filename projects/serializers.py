# apps/projects/serializers.py
from rest_framework import serializers
from .models import Project, ProjectGallery

# Serializer for gallery images
class ProjectGallerySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectGallery
        fields = "__all__"

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


# Main Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    featured_image_url = serializers.SerializerMethodField()
    gallery_images = ProjectGallerySerializer(many=True, read_only=True)  # This is the fix

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("user",)

    def get_featured_image_url(self, obj):
        request = self.context.get("request")
        if obj.featured_image and hasattr(obj.featured_image, "url"):
            return request.build_absolute_uri(obj.featured_image.url) if request else obj.featured_image.url
        return None

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "category",
            "excerpt",
            "technologies",
            "keywords",
            "tags",
            "featured_image",
            "featured_image_alt",
            "status",
            "project_type",
            "started_date",
            "completed_date",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    gallery_images = ProjectGallerySerializer(many=True, read_only=True)  # This is the fix

    class Meta:
        model = Project
        fields = "__all__"