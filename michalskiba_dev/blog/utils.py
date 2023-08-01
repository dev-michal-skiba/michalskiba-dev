from pathlib import Path

from django.conf import settings
from slugify import slugify

from blog.domain import ExtractedBlogPostInfo
from blog.post_converter import (
    get_content_html_text,
    get_content_text,
    get_lead_text,
    get_tags,
    get_title_text,
)


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


def get_blog_post_html_content(absolute_path: Path) -> str:
    with open(absolute_path, "r") as blog_post_file:
        html_content = blog_post_file.read()
    return html_content
