# apps/settings/serializers.py
from rest_framework import serializers
from config.serializers.base import BaseModelSerializer
from .models import Setting, SEOPageSetting, SitemapSetting, DisplaySetting

class SettingSerializer(BaseModelSerializer):
    class Meta:
        model = Setting
        fields = "__all__"


class SEOPageSettingSerializer(BaseModelSerializer):
    class Meta:
        model = SEOPageSetting
        fields = "__all__"


class SitemapSettingSerializer(BaseModelSerializer):
    class Meta:
        model = SitemapSetting
        fields = "__all__"



class DisplaySettingSerializer(BaseModelSerializer):
    class Meta:
        model = DisplaySetting
        fields = "__all__"
