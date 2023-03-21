from django.db import models


class BlogPostRaw(models.Model):
    content_path = models.CharField(max_length=64, unique=True)

    @property
    def is_processed(self) -> bool:
        # TODO check whether file is processed based on existence of processed blog post
        return False
