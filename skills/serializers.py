# apps/skills/serializers.py
from rest_framework import serializers
from .models import Skill, SubSkill
from core.utils.revalidate import trigger_revalidation

# ----------------------------
# SubSkill Serializer
# ----------------------------

class SubSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubSkill
        exclude = ["uploaded_by", "uploaded_ip"]
        read_only_fields = ["id", "created_at", "updated_at", "skill"]


# ----------------------------
# Skill Serializer
# ----------------------------

class SkillSerializer(serializers.ModelSerializer):
    subskills = SubSkillSerializer(many=True)

    class Meta:
        model = Skill
        exclude = ["uploaded_by", "uploaded_ip"]
        read_only_fields = ["id", "created_at", "updated_at"]

    # ----------------------------
    # CREATE
    # ----------------------------

    def create(self, validated_data):
        subskills_data = validated_data.pop("subskills", [])
        skill = Skill.objects.create(**validated_data)

        for subskill_data in subskills_data:
            SubSkill.objects.create(skill=skill, **subskill_data)

        trigger_revalidation(paths=["/"])
        return skill

    # ----------------------------
    # UPDATE
    # ----------------------------

    def update(self, instance, validated_data):
        subskills_data = validated_data.pop("subskills", None)
        instance.name = validated_data.get("name", instance.name)
        instance.icon = validated_data.get("icon", instance.icon)
        instance.is_public = validated_data.get("is_public", instance.is_public)
        instance.save()

        if subskills_data is not None:
            instance.subskills.all().delete()

            for subskill_data in subskills_data:
                SubSkill.objects.create(skill=instance, **subskill_data)

        trigger_revalidation(paths=["/"])
        return instance
