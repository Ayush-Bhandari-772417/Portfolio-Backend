# apps/creations/serializers.py
from rest_framework import serializers
from .models import Creation, Category
from core.utils.revalidate import trigger_revalidation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        category = super().create(validated_data)
        trigger_revalidation(paths=[
            "/categories",
        ])
        return category
    
    def update(self, instance, validated_data):
        category = super().update(instance, validated_data)
        trigger_revalidation(paths=[
            "/categories",
        ])
        return category


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
        instance = super().create(validated_data)
        self._trigger_revalidation(instance)
        return instance

    # ---------------- UPDATE ----------------
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self._trigger_revalidation(instance)
        return instance

    # ---------------- HELPER ----------------
    def _trigger_revalidation(self, instance):
        paths = [
            "/",
            "/creations",
            f"/creations/{instance.type}",
            f"/creations/{instance.type}/{instance.slug}",
            f"/creations/{instance.slug}",
        ]
        # ✅ Safely handle category
        if instance.category is not None:
            paths.append(f"/creations/{instance.category.id}")
            paths.append(f"/creations/{instance.category.id}/{instance.slug}")
        trigger_revalidation(paths=paths)