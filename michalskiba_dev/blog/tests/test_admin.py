from datetime import datetime
from typing import Callable
from unittest.mock import Mock, patch

import pytest
from django.test import Client
from django.urls import reverse
from freezegun import freeze_time

from blog.models import BlogPost, BlogPostRaw
from blog.tests.factories import BlogPostFactory


@pytest.fixture
def client(login_superuser: Callable[[Client], None]) -> Client:
    client = Client()
    login_superuser(client)
    return client


@pytest.mark.django_db
class TestBlogPostRawAdmin:
    @patch("blog.admin.create_blog_post_file", Mock())
    class TestConvertBlogPostRaw:
        @pytest.fixture
        def change_url(self) -> str:
            return reverse("admin:blog_blogpostraw_changelist")

        def test_blog_post_created(
            self, client: Client, change_url: str, blog_post_raw: BlogPostRaw
        ) -> None:
            data = {
                "action": "convert_blog_post_raw",
                "_selected_action": BlogPostRaw.objects.all().values_list("pk", flat=True),
            }
            assert BlogPost.objects.count() == 0

            client.post(change_url, data)

            assert BlogPost.objects.count() == 1
            blog_post = BlogPost.objects.first()
            assert isinstance(blog_post, BlogPost)
            assert blog_post.blog_post_raw == blog_post_raw
            assert blog_post.content_path == "test_raw_blog_post.html"
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

        def test_blog_post_updated(
            self, client: Client, change_url: str, blog_post_raw: BlogPostRaw
        ) -> None:
            data = {
                "action": "convert_blog_post_raw",
                "_selected_action": BlogPostRaw.objects.all().values_list("pk", flat=True),
            }
            blog_post = BlogPostFactory(
                blog_post_raw=blog_post_raw,
                content_path="test_path",
                slug="test-title",
                title="Test title",
                lead="Test lead",
            )
            assert BlogPost.objects.count() == 1
            assert blog_post.blog_post_raw == blog_post_raw
            assert blog_post.content_path == "test_path"
            assert blog_post.slug == "test-title"
            assert blog_post.title == "Test title"
            assert blog_post.lead == "Test lead"
            assert blog_post.tags.count() == 0

            client.post(change_url, data)

            blog_post.refresh_from_db()
            assert BlogPost.objects.count() == 1
            assert blog_post.blog_post_raw == blog_post_raw
            assert blog_post.content_path == "test_raw_blog_post.html"
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


@pytest.mark.django_db
class TestBlogPostAdmin:
    class TestReleaseAction:
        def test_release_info_set(
            self, blog_post: BlogPost, client: Client, test_datetime: datetime
        ) -> None:
            change_url = reverse("admin:blog_blogpost_changelist")
            data = {
                "action": "release",
                "_selected_action": BlogPost.objects.all().values_list("pk", flat=True),
            }
            assert blog_post.is_released is False
            assert blog_post.release_date is None

            with freeze_time(test_datetime):
                client.post(change_url, data)

            blog_post.refresh_from_db()
            assert blog_post.is_released is True
            assert blog_post.release_date == test_datetime

    class TestRevertReleaseAction:
        def test_release_info_cleared(
            self, blog_post: BlogPost, client: Client, test_datetime: datetime
        ) -> None:
            change_url = reverse("admin:blog_blogpost_changelist")
            data = {
                "action": "revert_release",
                "_selected_action": BlogPost.objects.all().values_list("pk", flat=True),
            }
            blog_post.is_released = True
            blog_post.release_date = test_datetime
            blog_post.save()
            assert blog_post.is_released is True
            assert blog_post.release_date == test_datetime

            client.post(change_url, data)

            blog_post.refresh_from_db()
            assert blog_post.is_released is False
            assert blog_post.release_date is None
