import os
from pathlib import Path

from django.conf import settings
from slugify import slugify

from blog.constants import MARKDOWN_IMAGES_REGEX
from blog.domain import ExtractedBlogPostInfo
from blog.raw_parser import (
    get_content_html_text,
    get_content_text,
    get_lead_text,
    get_tags,
    get_title_text,
)


def remove_files(file_paths_to_remove: list[Path]) -> None:
    for file_path in file_paths_to_remove:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)


def extract_images_absolute_paths_from_blog_post_raw_file(file_path: Path) -> list[Path]:
    images_absolute_paths: list[Path] = []
    content_text = get_content_text(file_path=file_path)
    matches = MARKDOWN_IMAGES_REGEX.findall(content_text)
    for match in matches:
        _, relative_path = match
        absolute_path = os.path.join(os.path.dirname(file_path), relative_path)
        absolute_path = os.path.normpath(absolute_path)
        images_absolute_paths.append(Path(absolute_path))
    return images_absolute_paths


def get_extracted_blog_post_info_from_blog_post_raw_file(file_path: Path) -> ExtractedBlogPostInfo:
    title = get_title_text(file_path=file_path)
    slug = slugify(title)
    lead = get_lead_text(file_path=file_path)
    tags: list[str] = get_tags(file_path=file_path)
    content = get_content_text(file_path)
    html_content = get_content_html_text(content_text=content)
    return ExtractedBlogPostInfo(
        title=title,
        slug=slug,
        lead=lead,
        tags=tags,
        html_content=html_content,
    )


def create_blog_post_file(content_path: str, html_content: str) -> None:
    file_path = settings.BLOG_POSTS_PATH / content_path
    with open(file_path, "w") as blog_post_file:
        blog_post_file.write(html_content)
