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
@patch("blog.management.commands.detect_new_post_files.convert_blog_post_raw")
class TestCommand:
    def test_nothing_happened_when_raw_and_blog_post_exist(
        self,
        convert_blog_post_raw_mock: Mock,
        blog_post: BlogPost,
        blog_post_raw: BlogPostRaw,
        caplog: LogCaptureFixture,
    ) -> None:
        call_command("detect_new_post_files")

        assert caplog.messages == ["Detecting new blog post files"]
        assert convert_blog_post_raw_mock.call_count == 0

    def test_warning_logged_when_raw_and_blog_post_does_not_exist(
        self, convert_blog_post_raw_mock: Mock, caplog: LogCaptureFixture
    ) -> None:
        call_command("detect_new_post_files")

        assert caplog.messages == [
            "Detecting new blog post files",
            'Missing blog post raw file "test_blog_post.md" for blog post file '
            '"test_blog_post.html"',
        ]
        assert convert_blog_post_raw_mock.call_count == 0

    def test_post_created_when_raw_exists_and_blog_post_does_not_exist(
        self,
        convert_blog_post_raw_mock: Mock,
        blog_post_raw: BlogPostRaw,
        caplog: LogCaptureFixture,
    ) -> None:
        assert BlogPost.objects.count() == 0

        call_command("detect_new_post_files")

        convert_blog_post_raw_mock.assert_called_once_with(blog_post_raw)
