from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse

from blog.models import BlogPost


@pytest.mark.django_db
class TestHome:
    def test_renders_home_template(self) -> None:
        client = Client()

        response = client.get("/")

        assert response.status_code == 200
        assert "blog/home.html" in (t.name for t in response.templates)


class TestAboutMe:
    def test_renders_about_me_template(self) -> None:
        client = Client()

        response = client.get("/about-me")

        assert response.status_code == 200
        assert "blog/about_me.html" in (t.name for t in response.templates)


@pytest.mark.django_db
class TestPost:
    def test_redirects_to_home_when_no_slug_match(self, blog_post: BlogPost) -> None:
        client = Client()

        response = client.get("/post/dummy-slug")

        assert response.status_code == 302
        assert response["Location"] == reverse("home")

    @patch("blog.context.get_blog_post_html_content", lambda path: "test content")
    def test_renders_post_template(self, blog_post_2: BlogPost) -> None:
        client = Client()
        blog_post_2.is_released = True
        blog_post_2.save()

        response = client.get(f"/post/{blog_post_2.slug}")

        assert response.status_code == 200
        assert "blog/post.html" in (t.name for t in response.templates)
