# apps/projects/serializers.py
from rest_framework import serializers
from config.serializers.base import BaseModelSerializer
from .models import Project, ProjectGallery

# Serializer for gallery images
class ProjectGallerySerializer(BaseModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectGallery
        fields = "__all__"

    def get_image_url(self, obj):
        return super().get_image_url(obj, 'image')


# Main Project Serializer
class ProjectSerializer(BaseModelSerializer):
    featured_image_url = serializers.SerializerMethodField()
    gallery_images = ProjectGallerySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("user",)

    def get_featured_image_url(self, obj):
        return super().get_image_url(obj, 'featured_image')
    

class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "id",
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