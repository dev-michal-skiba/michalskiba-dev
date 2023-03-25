from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest

from blog.models import BlogPostRaw
from blog.tests.factories import BlogPostRawFactory


@pytest.mark.django_db
class TestBlogPostRaw:
    def test_is_processed(self, blog_post_raw: BlogPostRawFactory) -> None:
        assert blog_post_raw.is_processed is False

    def test_absolute_path(self, blog_post_raw: BlogPostRawFactory) -> None:
        expected_path = blog_post_raw.BASE_CONTENT_PATH / blog_post_raw.content_path
        assert blog_post_raw.absolute_path == expected_path

    def test_str(self, blog_post_raw: BlogPostRawFactory) -> None:
        assert str(blog_post_raw) == blog_post_raw.content_path


@pytest.mark.django_db
@patch("blog.utils.os.remove")
class TestBlogPostRawPreDeleteSignal:
    def test_database_record_and_files_are_removed(
        self, os_remove_mock: Mock, blog_post_raw: BlogPostRawFactory, test_working_directory: Path
    ) -> None:
        blog_post_raw.delete()

        assert BlogPostRaw.objects.count() == 0
        calls = [
            call(test_working_directory / "blog/tests/data/raw/test_raw_blog_post.md"),
            call(test_working_directory / "blog/tests/data/images/empty_shelves.jpg"),
            call(test_working_directory / "blog/tests/data/images/empty_shelves_grayscale.png"),
            call(test_working_directory / "blog/tests/data/images/empty_shelves_edges.png"),
            call(test_working_directory / "blog/tests/data/images/empty_shelves_erosion.png"),
            call(test_working_directory / "blog/tests/data/images/empty_shelves_dilation.png"),
        ]
        os_remove_mock.assert_has_calls(calls)
