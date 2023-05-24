import logging
import os
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from blog.models import BlogPostRaw

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = f"Detect new blog post raw files in {settings.BLOG_POSTS_RAW_PATH}"

    def handle(self, *args: list[Any], **options: dict[str, Any]) -> None:
        logger.info("Detecting new blog post raw files")
        for root, sub_dirs, file_names in os.walk(settings.BLOG_POSTS_RAW_PATH):
            for file_name in file_names:
                file_path = f"{root}/{file_name}"
                relative_file_path = os.path.relpath(file_path, settings.BLOG_POSTS_RAW_PATH)
                blog_post_raw, created = BlogPostRaw.objects.get_or_create(
                    content_path=relative_file_path
                )
                if created:
                    logger.info(
                        f"Blog post raw for {relative_file_path} "
                        f"created with pk {blog_post_raw.pk}"
                    )
