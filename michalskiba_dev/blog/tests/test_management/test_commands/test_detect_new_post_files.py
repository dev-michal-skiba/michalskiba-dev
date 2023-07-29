from unittest.mock import Mock, patch

import pytest
from _pytest.logging import LogCaptureFixture
from django.conf import settings
from django.core.management import call_command

from blog.models import BlogPost, BlogPostRaw

OS_WALK: list[tuple[str, list[str], list[str]]] = [
    (f"{settings.BLOG_POSTS_PATH}/test_root", [], ["test_blog_post.html"])
]


@pytest.mark.django_db
@patch("blog.management.commands.detect_new_post_files.os.walk", Mock(return_value=OS_WALK))
class TestCommand:
    def test_nothing_happened_when_raw_and_blog_post_exist(
        self, blog_post: BlogPost, blog_post_raw: BlogPostRaw, caplog: LogCaptureFixture
    ) -> None:
        call_command("detect_new_post_files")

        assert caplog.messages == ["Detecting new blog post files"]

    def test_warning_logged_when_raw_and_blog_post_does_not_exist(
        self, caplog: LogCaptureFixture
    ) -> None:
        call_command("detect_new_post_files")

        assert caplog.messages == [
            "Detecting new blog post files",
            'Missing blog post raw file "test_blog_post.md" for blog post file '
            '"test_blog_post.html"',
        ]

    def test_post_created_when_raw_exists_and_blog_post_does_not_exist(
        self, blog_post_raw: BlogPostRaw, caplog: LogCaptureFixture
    ) -> None:
        assert BlogPost.objects.count() == 0

        call_command("detect_new_post_files")

        assert BlogPost.objects.count() == 1
        blog_post = BlogPost.objects.first()
        assert isinstance(blog_post, BlogPost)
        assert blog_post.blog_post_raw == blog_post_raw
        assert blog_post.content_path == "test_blog_post.html"
        assert blog_post.slug == (
            "some-title-title-title-title-title-title-title-title-title-title-title-title-"
            "title-title-title-title-title-title-title-title-tit"
        )
        assert blog_post.title == (
            "Some title title title title title title title title title title title title "
            "title title title title title title title title tit"
        )
        assert blog_post.lead == "Some xy" + 101 * " lead"
        assert blog_post.tags.count() == 3
        assert caplog.messages == [
            "Detecting new blog post files",
            'Created blog post in database for "test_blog_post.html" file',
        ]
