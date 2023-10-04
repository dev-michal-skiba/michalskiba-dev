from __future__ import annotations

import bcrypt
from django.db import models


class DemoUser(models.Model):
    username = models.CharField(max_length=64, unique=True)
    hashed_password = models.CharField(max_length=128)

    @classmethod
    def login(cls, username: str, password: str) -> DemoUser | None:
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
