import logging
import os
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from blog.models import BlogPost, BlogPostRaw, Tag
from blog.utils import get_extracted_blog_post_info_from_blog_post_raw_file

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = f"Detect new blog post files in {settings.BLOG_POSTS_PATH}"

    def handle(self, *args: list[Any], **options: dict[str, Any]) -> None:
        logger.info("Detecting new blog post files")
        for root, sub_dirs, file_names in os.walk(settings.BLOG_POSTS_PATH):
            for file_name in file_names:
                blog_post = BlogPost.objects.filter(content_path=file_name).first()
                if blog_post:
                    continue
                expected_blog_post_file_name = file_name.replace("html", "md")
                blog_post_raw = BlogPostRaw.objects.filter(
                    content_path=expected_blog_post_file_name
                ).first()
                if not blog_post_raw:
                    logger.warning(
                        'Missing blog post raw file "%s" for blog post file "%s"',
                        expected_blog_post_file_name,
                        file_name,
                    )
                    continue
                extracted_blog_post_info = get_extracted_blog_post_info_from_blog_post_raw_file(
                    blog_post_raw.absolute_path
                )
                tags: list[Tag] = []
                for text_tag in extracted_blog_post_info.tags:
                    tag, _ = Tag.objects.get_or_create(name=text_tag)
                    tags.append(tag)
                blog_post = BlogPost.objects.create(
                    blog_post_raw=blog_post_raw,
                    content_path=file_name,
                    slug=extracted_blog_post_info.slug,
                    title=extracted_blog_post_info.title,
                    lead=extracted_blog_post_info.lead,
                )
                blog_post.tags.set(tags)
                logger.info('Created blog post in database for "%s" file', file_name)