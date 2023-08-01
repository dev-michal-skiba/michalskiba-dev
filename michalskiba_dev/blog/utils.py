from pathlib import Path

from django.conf import settings

from blog.models import BlogPost, BlogPostRaw, Tag
from blog.post_converter import get_extracted_blog_post_from_blog_post_raw_file


def convert_blog_post_raw(blog_post_raw: BlogPostRaw) -> None:
    extracted_blog_post = get_extracted_blog_post_from_blog_post_raw_file(
        blog_post_raw.absolute_path
    )
    create_blog_post_file(
        content_path=extracted_blog_post.content_path,
        html_content=extracted_blog_post.html_content,
    )
    blog_post, _ = BlogPost.objects.update_or_create(
        blog_post_raw=blog_post_raw,
        defaults={
            "content_path": extracted_blog_post.content_path,
            "slug": extracted_blog_post.slug,
            "title": extracted_blog_post.title,
            "lead": extracted_blog_post.lead,
        },
    )
    blog_post.tags.clear()
    tags = get_or_create_tags(extracted_blog_post.tags)
    blog_post.tags.set(tags)


def create_blog_post_file(content_path: str, html_content: str) -> None:
    file_path = settings.BLOG_POSTS_PATH / content_path
    with open(file_path, "w") as blog_post_file:
        blog_post_file.write(html_content)


def get_or_create_tags(tags: list[str]) -> list[Tag]:
    result_tags: list[Tag] = []
    for text_tag in tags:
        tag, _ = Tag.objects.get_or_create(name=text_tag)
        result_tags.append(tag)
    return result_tags


def get_blog_post_html_content(absolute_path: Path) -> str:
    with open(absolute_path, "r") as blog_post_file:
        html_content = blog_post_file.read()
    return html_content
