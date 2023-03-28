from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest

from blog.models import BlogPost, BlogPostBase, BlogPostRaw


class BlogPostBaseTests:
    class Test:
        def test_absolute_path(self, instance: BlogPostBase) -> None:
            expected_path = instance.BASE_CONTENT_PATH / instance.content_path
            assert instance.absolute_path == expected_path

        def test_str(self, instance: BlogPostBase) -> None:
            assert str(instance) == instance.content_path


@pytest.mark.django_db
class TestBlogPostRaw(BlogPostBaseTests):
    @pytest.fixture
    def instance(self, blog_post_raw: BlogPostRaw) -> BlogPostRaw:
        return blog_post_raw

    def test_is_processed(self, blog_post_raw: BlogPostRaw) -> None:
        assert blog_post_raw.is_processed is False


@pytest.mark.django_db
class TestBlogPost(BlogPostBaseTests):
    @pytest.fixture
    def instance(self, blog_post: BlogPost) -> BlogPost:
        return blog_post


@pytest.mark.django_db
@patch("blog.utils.os.remove")
class TestBlogPostRawPreDeleteSignal:
    def test_database_record_and_files_are_removed(
        self, os_remove_mock: Mock, blog_post_raw: BlogPostRaw, test_working_directory: Path
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


@pytest.mark.django_db
@patch("blog.utils.os.remove")
class TestBlogPostPreDeleteSignal:
    def test_database_record_and_files_are_removed(
        self, os_remove_mock: Mock, blog_post: BlogPost, test_working_directory: Path
    ) -> None:
        blog_post.delete()

        assert BlogPost.objects.count() == 0
        calls = [
            call(test_working_directory / "blog/tests/data/posts/test_blog_post.html"),
        ]
        os_remove_mock.assert_has_calls(calls)
