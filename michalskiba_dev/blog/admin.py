from datetime import datetime, timezone

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from blog.models import BlogPost, BlogPostRaw, Tag
from blog.utils import (
    create_blog_post_file,
    get_extracted_blog_post_info_from_blog_post_raw_file,
)


class BlogPostRawAdmin(admin.ModelAdmin[BlogPostRaw]):
    actions = ["process_raw_file"]
    list_display = ["content_path", "is_processed"]

    @admin.action(description="Process raw file(s)")
    def process_raw_file(self, request: HttpRequest, queryset: QuerySet[BlogPostRaw]) -> None:
        for blog_post_raw in queryset:
            extracted_blog_post_info = get_extracted_blog_post_info_from_blog_post_raw_file(
                blog_post_raw.absolute_path
            )
            blog_post_content_path = blog_post_raw.content_path.replace(".md", ".html")
            create_blog_post_file(
                content_path=blog_post_content_path,
                html_content=extracted_blog_post_info.html_content,
            )
            tags: list[Tag] = []
            for text_tag in extracted_blog_post_info.tags:
                tag, _ = Tag.objects.get_or_create(name=text_tag)
                tags.append(tag)
            blog_post, _ = BlogPost.objects.update_or_create(
                blog_post_raw=blog_post_raw,
                defaults={
                    "content_path": blog_post_content_path,
                    "slug": extracted_blog_post_info.slug,
                    "title": extracted_blog_post_info.title,
                    "lead": extracted_blog_post_info.lead,
                },
            )
            blog_post.tags.set(tags)


class BlogPostAdmin(admin.ModelAdmin[BlogPost]):
    actions = ["release", "revert_release"]
    list_display = ["title", "blog_post_raw", "is_released", "release_date"]

    @admin.action(description="Release blog post")
    def release(self, request: HttpRequest, queryset: QuerySet[BlogPost]) -> None:
        queryset.update(is_released=True, release_date=datetime.now(timezone.utc))

    @admin.action(description="Revert blog post release")
    def revert_release(self, request: HttpRequest, queryset: QuerySet[BlogPost]) -> None:
        queryset.update(is_released=False, release_date=None)


admin.site.register(BlogPostRaw, BlogPostRawAdmin)
admin.site.register(Tag)
admin.site.register(BlogPost, BlogPostAdmin)
