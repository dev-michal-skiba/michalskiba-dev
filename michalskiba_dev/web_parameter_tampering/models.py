from uuid import uuid4

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    hashed_password = models.CharField(max_length=128)


class PressApplication(models.Model):
    user = models.OneToOneField(User, related_name="press_application", on_delete=models.CASCADE)
    organization = models.CharField(max_length=64)
    note = models.CharField(max_length=1024)
    accepted = models.BooleanField(default=False)
    accreditation_code = models.CharField(max_length=36, default=uuid4)
