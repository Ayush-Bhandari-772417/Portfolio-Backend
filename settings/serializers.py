# apps/settings/serializers.py
from rest_framework import serializers
from .models import Setting, SEOPageSetting, SitemapSetting, DisplaySetting
from core.utils.revalidate import trigger_revalidation

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = "__all__"

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        trigger_revalidation(paths=["/", "/projects", "/blogs",])
        return instance


class SEOPageSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOPageSetting
        fields = "__all__"

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        trigger_revalidation(paths=["/", "/projects", "/blogs",])
        return instance


class SitemapSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitemapSetting
        fields = "__all__"

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        trigger_revalidation(paths=["/"])
        return instance



class DisplaySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplaySetting
        fields = "__all__"

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        trigger_revalidation(paths=["/", "/projects", "/blogs","/creations",])
        return instance
