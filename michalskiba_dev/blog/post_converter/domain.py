from pathlib import Path

from slugify import slugify

from .sections import (
    get_content_html_text,
    get_content_text,
    get_lead_text,
    get_tags,
    get_title_text,
)
from .types import ExtractedBlogPost


def get_extracted_blog_post_from_blog_post_raw_file(file_path: Path) -> ExtractedBlogPost:
    content_path = file_path.stem + ".html"
    title = get_title_text(file_path=file_path)
    slug = slugify(title)
    lead = get_lead_text(file_path=file_path)
    tags: list[str] = get_tags(file_path=file_path)
    content = get_content_text(file_path)
    html_content = get_content_html_text(content_text=content)
    return ExtractedBlogPost(
        content_path=content_path,
        title=title,
        slug=slug,
        lead=lead,
        tags=tags,
        html_content=html_content,
    )
