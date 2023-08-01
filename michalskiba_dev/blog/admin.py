from datetime import datetime, timezone

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from blog.models import BlogPost, BlogPostRaw, Tag
from blog.utils import convert_blog_post_raw


class BlogPostRawAdmin(admin.ModelAdmin[BlogPostRaw]):
    actions = ["convert_blog_post_raw"]
    list_display = ["content_path", "is_converted"]

    @admin.action(description="Convert blog post raw file(s)")
    def convert_blog_post_raw(self, request: HttpRequest, queryset: QuerySet[BlogPostRaw]) -> None:
        for blog_post_raw in queryset:
            convert_blog_post_raw(blog_post_raw)


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
