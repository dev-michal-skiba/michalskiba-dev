from __future__ import annotations

from uuid import uuid4

from django.db import models

from demo.models import DemoUser


class PressApplication(models.Model):
    user = models.OneToOneField(
        DemoUser, related_name="press_application", on_delete=models.CASCADE
    )
    organization = models.CharField(max_length=64)
    note = models.CharField(max_length=1024)
    accepted = models.BooleanField(default=False)
    accreditation_code = models.CharField(max_length=36, default=uuid4)

    def __str__(self) -> str:
        return f"Press application <{self.user.username}>"
