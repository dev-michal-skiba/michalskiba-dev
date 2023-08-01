from datetime import datetime
from typing import Callable
from unittest.mock import Mock, patch

import pytest
from django.test import Client
from django.urls import reverse
from freezegun import freeze_time

from blog.models import BlogPost, BlogPostRaw


@pytest.fixture
def client(login_superuser: Callable[[Client], None]) -> Client:
    client = Client()
    login_superuser(client)
    return client


@pytest.mark.django_db
class TestBlogPostRawAdmin:
    @patch("blog.utils.create_blog_post_file", Mock())
    @patch("blog.admin.convert_blog_post_raw")
    class TestConvertBlogPostRaw:
        @pytest.fixture
        def change_url(self) -> str:
            return reverse("admin:blog_blogpostraw_changelist")

        def test_blog_post_created(
            self,
            convert_blog_post_raw_mock: Mock,
            client: Client,
            change_url: str,
            blog_post_raw: BlogPostRaw,
        ) -> None:
            data = {
                "action": "convert_blog_post_raw",
                "_selected_action": BlogPostRaw.objects.all().values_list("pk", flat=True),
            }

            client.post(change_url, data)

            convert_blog_post_raw_mock.assert_called_once_with(blog_post_raw)


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
