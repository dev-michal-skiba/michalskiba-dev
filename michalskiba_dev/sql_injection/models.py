from django.db import models


class ParcelStore(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    opening_hours = models.CharField(max_length=64)
    access_code = models.CharField(max_length=16)

    def __str__(self) -> str:
        return self.name
