# apps/skills/models.py
from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)  # store icon name e.g., "FaCode"
    is_public = models.BooleanField(default=True)  # control visibility in public API
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SubSkill(models.Model):
    skill = models.ForeignKey(Skill, related_name="subskills", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "Python", "C++"
    icon = models.CharField(max_length=100, blank=True, null=True)  # e.g., "FaPython"
    level = models.CharField(
        max_length=50,
        choices=[("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Pro", "Pro"), ("Expert", "Expert")],
        default="Beginner",
    )
    rating = models.PositiveIntegerField(default=0)  # 1–5 stars
    is_public = models.BooleanField(default=True)  # control visibility in public API
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.level})"
