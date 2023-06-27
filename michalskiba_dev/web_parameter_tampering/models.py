from __future__ import annotations

from uuid import uuid4

import bcrypt
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    hashed_password = models.CharField(max_length=128)

    @classmethod
    def login(cls, username: str, password: str) -> User | None:
        user = cls.objects.filter(username=username).first()
        if not user:
            return None
        is_password_correct = bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8")
        )
        if not is_password_correct:
            return None
        return user

    def __str__(self) -> str:
        return self.username


class PressApplication(models.Model):
    user = models.OneToOneField(User, related_name="press_application", on_delete=models.CASCADE)
    organization = models.CharField(max_length=64)
    note = models.CharField(max_length=1024)
    accepted = models.BooleanField(default=False)
    accreditation_code = models.CharField(max_length=36, default=uuid4)

    def __str__(self) -> str:
        return f"Press application <{self.user.username}>"
