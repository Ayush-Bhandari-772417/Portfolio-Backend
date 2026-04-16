# apps/creations/serializers.py
from rest_framework import serializers
from config.serializers.base import BaseModelSerializer
from .models import Creation, Category


class CategorySerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CreationSerializer(BaseModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Creation
        fields = '__all__'
        read_only_fields = ['id', 'user', 'posted_date']

    def get_featured_image_url(self, obj):
        return self.get_image_url(obj, 'featured_image')

    # ---------------- CREATE ----------------
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
        

class CreationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Creation
        fields = [
            "id",
            "title",
            "slug",
            "language",
            "featured_image",
            "featured_image_alt",
            "type",
            "category",
            "keywords",
            "excerpt",
            "written_date",
            "updated_date",
        ]


class CreationDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Creation
        fields = "__all__"