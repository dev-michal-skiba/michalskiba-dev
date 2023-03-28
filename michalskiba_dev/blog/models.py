from pathlib import Path
from typing import Any

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from blog.utils import extract_images_absolute_paths_from_markdown_file, remove_files


class BlogPostRaw(models.Model):
    content_path = models.CharField(max_length=64, unique=True)

    BASE_CONTENT_PATH: Path = settings.BLOG_POSTS_RAW_PATH

    @property
    def is_processed(self) -> bool:
        # TODO check whether file is processed based on existence of processed blog post
        return False

    @property
    def absolute_path(self) -> Path:
        return self.BASE_CONTENT_PATH / self.content_path

    def __str__(self) -> str:
        return self.content_path


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)


@receiver(pre_delete, sender=BlogPostRaw, dispatch_uid="blog_post_raw_pre_delete_signal")
def blog_post_raw_pre_delete_signal(instance: BlogPostRaw, **kwargs: dict[str, Any]) -> None:
    images_absolute_paths = extract_images_absolute_paths_from_markdown_file(
        instance.absolute_path
    )
    files_to_remove = [instance.absolute_path] + images_absolute_paths
    remove_files(files_to_remove)
