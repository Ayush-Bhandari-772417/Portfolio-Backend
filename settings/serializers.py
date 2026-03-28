# apps/settings/serializers.py
from rest_framework import serializers
from .models import Setting, SEOPageSetting, SitemapSetting, DisplaySetting

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = "__all__"

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class SEOPageSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOPageSetting
        fields = "__all__"

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class SitemapSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitemapSetting
        fields = "__all__"

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



class DisplaySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplaySetting
        fields = "__all__"

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
