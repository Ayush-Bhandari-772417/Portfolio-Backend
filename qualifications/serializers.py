# apps/qualifications/serializers.py
from rest_framework import serializers
from .models import Qualification
from config.serializers.base import BaseModelSerializer

class QualificationSerializer(BaseModelSerializer):
    class Meta:
        model = Qualification
        fields = "__all__"
