# apps/qualifications/models.py
from django.db import models
from django.conf import settings

class Qualification(models.Model):
    board_name = models.CharField(max_length=255)                       # SEE                               # Bachelor
    school_name = models.CharField(max_length=255)                      # Little Angels'                    # IOE Thapathali Campus
    school_url = models.URLField(blank=True, null=True)                 # link of Little Angels'            # link of IOE Thapathali Campus
    location = models.CharField(max_length=255)                         # location name of Little Angels'   # location name of IOE Thapathali Campus
    location_url = models.URLField(blank=True, null=True)               # location url of Little Angels'    # location URL of IOE Thapathali Campus
    enrolled_year = models.IntegerField()                               # 2017                              # 2021
    passed_year = models.IntegerField(blank=True, null=True)            # 2018                              # present (because not complete till now)
    grade = models.CharField(max_length=50, blank=True, null=True)      # A                                 # --- (because not complete till now)
    description = models.CharField(max_length=255, blank=True, null=True)  # description about the school   # description about the college
    is_public = models.BooleanField(default=False)

    uploaded_ip = models.GenericIPAddressField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.school_name} ({self.enrolled_year}-{self.passed_year or 'Present'})"
