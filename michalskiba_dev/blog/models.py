from django.db import models


class BlogPostRaw(models.Model):
    content_path = models.CharField(max_length=64, unique=True)
