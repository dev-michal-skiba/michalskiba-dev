from pathlib import Path
from typing import Any, Self

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from blog.utils import (
    extract_images_absolute_paths_from_blog_post_raw_file,
    remove_files,
)


class BlogPostBase(models.Model):
    content_path = models.CharField(max_length=64, unique=True)

    BASE_CONTENT_PATH: Path = Path("")

    class Meta:
        abstract = True

    @property
    def absolute_path(self) -> Path:
        return self.BASE_CONTENT_PATH / self.content_path

    def __str__(self) -> str:
        return self.content_path


class BlogPostRaw(BlogPostBase):
    BASE_CONTENT_PATH: Path = settings.BLOG_POSTS_RAW_PATH

    @property
    def is_processed(self) -> bool:
        return hasattr(self, "blog_post") and isinstance(self.blog_post, BlogPost)


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self) -> str:
        return self.name


class BlogPostManager(models.Manager[Any]):
    def filter_for_display(self, user: User | AnonymousUser) -> QuerySet[Any] | Self:
        if user.is_superuser:
            return self.all()
        return self.filter(is_released=True)


class BlogPost(BlogPostBase):
    creation_date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField(blank=True, null=True)
    is_released = models.BooleanField(default=False)
    slug = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=64, unique=True)
    lead = models.TextField(max_length=512)
    tags = models.ManyToManyField(Tag, related_name="blog_posts")
    blog_post_raw = models.OneToOneField(
        BlogPostRaw, on_delete=models.CASCADE, related_name="blog_post"
    )

    BASE_CONTENT_PATH: Path = settings.BLOG_POSTS_PATH
    objects = BlogPostManager()

    @property
    def release_date_for_display(self) -> str:
        if self.release_date:
            return self.release_date.strftime("%Y.%m.%d")
        return "NOT RELEASED"

    @property
    def tags_for_display(self) -> str:
        return ", ".join(self.tags.values_list("name", flat=True))


@receiver(pre_delete, sender=BlogPostRaw, dispatch_uid="blog_post_raw_pre_delete_signal")
def blog_post_raw_pre_delete_signal(instance: BlogPostRaw, **kwargs: dict[str, Any]) -> None:
    images_absolute_paths = extract_images_absolute_paths_from_blog_post_raw_file(
        instance.absolute_path
    )
    files_to_remove = [instance.absolute_path] + images_absolute_paths
    remove_files(files_to_remove)


@receiver(pre_delete, sender=BlogPost, dispatch_uid="blog_post_pre_delete_signal")
def blog_post_pre_delete_signal(instance: BlogPost, **kwargs: dict[str, Any]) -> None:
    files_to_remove = [instance.absolute_path]
    remove_files(files_to_remove)