from django.db import models


class Flag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
