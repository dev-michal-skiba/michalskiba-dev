from datetime import datetime, timezone
from unittest.mock import Mock, call, patch

import pytest
from django.conf import settings
from django.contrib.auth.models import User

from blog.models import BlogPost, BlogPostBase, BlogPostRaw, Tag
from blog.tests.factories import TagFactory


@pytest.mark.django_db
class TestBlogPostManager:
    class TestFilterForDisplay:
        def test_for_superuser(
            self, superuser: User, blog_post: BlogPost, blog_post_2: BlogPost
        ) -> None:
            blog_post_2.is_released = True
            blog_post_2.save()

            queryset = BlogPost.objects.filter_for_display(superuser)

            assert queryset.count() == 2

        def test_for_user(self, user: User, blog_post: BlogPost, blog_post_2: BlogPost) -> None:
            blog_post_2.is_released = True
            blog_post_2.save()

            queryset = BlogPost.objects.filter_for_display(user)

            assert queryset.count() == 1


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

    def test_is_converted_when_blog_post_doesnt_exist(self, instance: BlogPostRaw) -> None:
        assert instance.is_converted is False

    def test_is_converted_when_blog_post_exists(
        self, instance: BlogPostRaw, blog_post: BlogPost
    ) -> None:
        assert instance.is_converted is True


@pytest.mark.django_db
class TestBlogPost(BlogPostBaseTests):
    @pytest.fixture
    def instance(self, blog_post: BlogPost) -> BlogPost:
        return blog_post

    def test_release_date_for_display(self, blog_post: BlogPost) -> None:
        blog_post.release_date = datetime(year=2023, month=5, day=8, tzinfo=timezone.utc)
        blog_post.save()

        assert blog_post.release_date_for_display == "2023.05.08"

    def test_release_date_for_display_for_null_value(self, blog_post: BlogPost) -> None:
        assert blog_post.release_date_for_display == "NOT RELEASED"

    def test_tags_for_display(self, blog_post: BlogPost) -> None:
        tag_1 = TagFactory(name="tag 1")
        tag_2 = TagFactory(name="tag 2")
        blog_post.tags.add(tag_1)
        blog_post.tags.add(tag_2)
        blog_post.save()

        assert blog_post.tags_for_display == "tag 1, tag 2"


@pytest.mark.django_db
@patch("blog.utils.os.remove")
class TestBlogPostRawPreDeleteSignal:
    def test_database_record_and_files_are_removed(
        self, os_remove_mock: Mock, blog_post_raw: BlogPostRaw
    ) -> None:
        blog_post_raw.delete()

        assert BlogPostRaw.objects.count() == 0
        calls = [
            call(settings.BLOG_POSTS_RAW_PATH / "test_raw_blog_post.md"),
            call(settings.BLOG_POSTS_IMAGES_PATH / "empty_shelves.jpg"),
            call(settings.BLOG_POSTS_IMAGES_PATH / "empty_shelves_grayscale.png"),
            call(settings.BLOG_POSTS_IMAGES_PATH / "empty_shelves_edges.png"),
            call(settings.BLOG_POSTS_IMAGES_PATH / "empty_shelves_erosion.png"),
            call(settings.BLOG_POSTS_IMAGES_PATH / "empty_shelves_dilation.png"),
        ]
        os_remove_mock.assert_has_calls(calls)


@pytest.mark.django_db
@patch("blog.utils.os.remove")
class TestBlogPostPreDeleteSignal:
    def test_database_record_and_files_are_removed(
        self, os_remove_mock: Mock, blog_post: BlogPost
    ) -> None:
        blog_post.delete()

        assert BlogPost.objects.count() == 0
        calls = [
            call(settings.BLOG_POSTS_PATH / "test_blog_post.html"),
        ]
        os_remove_mock.assert_has_calls(calls)


@pytest.mark.django_db
class TestTag:
    def test_str(self, tag: Tag) -> None:
        assert str(tag) == tag.name
