# apps/experience/serializers.py
from .models import Experience
from config.serializers.base import BaseModelSerializer

class ExperienceSerializer(BaseModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
