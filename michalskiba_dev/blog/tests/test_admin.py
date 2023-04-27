from typing import Callable
from unittest.mock import Mock, patch

import pytest
from django.test import Client
from django.urls import reverse

from blog.models import BlogPost, BlogPostRaw
from blog.tests.factories import BlogPostFactory


@pytest.mark.django_db
@patch("blog.admin.create_blog_post_file", Mock())
class TestProcessRawFile:
    @pytest.fixture
    def client(self, login_superuser: Callable[[Client], None]) -> Client:
        client = Client()
        login_superuser(client)
        return client

    @pytest.fixture
    def change_url(self) -> str:
        return reverse("admin:blog_blogpostraw_changelist")

    def test_blog_post_created(
        self, client: Client, change_url: str, blog_post_raw: BlogPostRaw
    ) -> None:
        data = {
            "action": "process_raw_file",
            "_selected_action": BlogPostRaw.objects.all().values_list("pk", flat=True),
        }
        assert BlogPost.objects.count() == 0

        client.post(change_url, data)

        assert BlogPost.objects.count() == 1
        blog_post = BlogPost.objects.first()
        assert isinstance(blog_post, BlogPost)
        assert blog_post.blog_post_raw == blog_post_raw
        assert blog_post.content_path == "test_raw_blog_post.html"
        assert blog_post.slug == "some-title-title-title-title-title-title-title-title-title-title"
        assert (
            blog_post.title == "Some title title title title title title title title title title"
        )
        assert blog_post.lead == "Some xy" + 101 * " lead"
        assert blog_post.tags.count() == 3

    def test_blog_post_updated(
        self, client: Client, change_url: str, blog_post_raw: BlogPostRaw
    ) -> None:
        data = {
            "action": "process_raw_file",
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
        assert blog_post.slug == "some-title-title-title-title-title-title-title-title-title-title"
        assert (
            blog_post.title == "Some title title title title title title title title title title"
        )
        assert blog_post.lead == "Some xy" + 101 * " lead"
        assert blog_post.tags.count() == 3
