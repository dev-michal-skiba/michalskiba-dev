from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest
from django.test import Client
from django.urls import reverse

from blog.models import BlogPost
from blog.tests.factories import TagFactory
from blog.views import _get_home_context, _get_post_context


@pytest.mark.django_db
class TestGetHomeContext:
    def test_correct_blog_posts_fields(self, blog_post: BlogPost) -> None:
        blog_post.release_date = datetime(year=2023, month=5, day=8, tzinfo=timezone.utc)
        blog_post.tags.add(TagFactory(name="tag 1"))
        blog_post.tags.add(TagFactory(name="tag 2"))
        blog_post.save()
        request = Mock()

        context = _get_home_context(request)

        assert len(context["blog_posts"]) == 1
        assert context["blog_posts"][0] == {
            "title": blog_post.title,
            "release_date": "2023.05.08",
            "tags": "tag 1, tag 2",
            "link": "/post/test-slug",
            "lead": blog_post.lead,
        }

    def test_blog_posts_ordered_descending(
        self, blog_post: BlogPost, blog_post_2: BlogPost
    ) -> None:
        blog_post.release_date = datetime(year=2023, month=5, day=8, tzinfo=timezone.utc)
        blog_post.save()
        blog_post_2.release_date = datetime(year=2023, month=5, day=9, tzinfo=timezone.utc)
        blog_post_2.save()

        request = Mock()

        context = _get_home_context(request)

        assert len(context["blog_posts"]) == 2
        assert context["blog_posts"][0]["title"] == blog_post_2.title
        assert context["blog_posts"][1]["title"] == blog_post.title

    def test_not_released_blog_post_included_at_top_for_superuser(
        self, blog_post: BlogPost, blog_post_2: BlogPost
    ) -> None:
        blog_post.release_date = datetime(year=2023, month=5, day=8, tzinfo=timezone.utc)
        blog_post.save()

        request = Mock()

        context = _get_home_context(request)

        assert len(context["blog_posts"]) == 2
        assert context["blog_posts"][0]["title"] == blog_post_2.title
        assert context["blog_posts"][1]["title"] == blog_post.title


@pytest.mark.django_db
class TestHome:
    def test_renders_home_template(self) -> None:
        client = Client()

        response = client.get("/")

        assert response.status_code == 200
        assert "home.html" in (t.name for t in response.templates)


class TestAboutMe:
    def test_renders_about_me_template(self) -> None:
        client = Client()

        response = client.get("/about-me")

        assert response.status_code == 200
        assert "about_me.html" in (t.name for t in response.templates)


@pytest.mark.django_db
@patch("blog.views.get_blog_post_html_content", lambda path: "test content")
class TestGetPostContext:
    def test_correct_context(self, blog_post: BlogPost) -> None:
        context = _get_post_context(blog_post)

        assert context == {
            "blog_post": {
                "title": blog_post.title,
                "lead": blog_post.lead,
                "tags": blog_post.tags_for_display,
                "html_content": "test content",
                "release_date": blog_post.release_date_for_display,
            }
        }


@pytest.mark.django_db
class TestPost:
    def test_redirects_to_home_when_no_slug_match(self, blog_post: BlogPost) -> None:
        client = Client()

        response = client.get("/post/dummy-slug")

        assert response.status_code == 302
        assert response["Location"] == reverse("home")

    @patch("blog.views.get_blog_post_html_content", lambda path: "test content")
    def test_renders_post_template(self, blog_post_2: BlogPost) -> None:
        client = Client()
        blog_post_2.is_released = True
        blog_post_2.save()

        response = client.get(f"/post/{blog_post_2.slug}")

        assert response.status_code == 200
        assert "post.html" in (t.name for t in response.templates)
