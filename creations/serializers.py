# apps/creations/serializers.py
from rest_framework import serializers
from .models import Creation, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CreationSerializer(serializers.ModelSerializer):
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
        request = self.context.get("request")
        if obj.featured_image:
            return request.build_absolute_uri(obj.featured_image.url)
        return None

    # ---------------- CREATE ----------------
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    # ---------------- UPDATE ----------------
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        

class CreationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Creation
        fields = [
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