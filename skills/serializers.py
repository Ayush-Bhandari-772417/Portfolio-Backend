# apps/skills/serializers.py
from rest_framework import serializers
from .models import Skill, SubSkill  # and SubSkill if you created it
from core.utils.revalidate import trigger_revalidation

class SubSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSkill
        fields = "__all__"

    def create(self, validated_data):
        subskill = super().create(validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return subskill
    
    def update(self, instance, validated_data):
        subskill = super().update(instance, validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return subskill


class SkillSerializer(serializers.ModelSerializer):
    subskills = SubSkillSerializer(many=True, read_only=True)  # Reverse relation via related_name

    class Meta:
        model = Skill
        fields = "__all__"

    def create(self, validated_data):
        skill = super().create(validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return skill
    
    def update(self, instance, validated_data):
        skill = super().update(instance, validated_data)
        trigger_revalidation(paths=[
            "/",
        ])
        return skill
