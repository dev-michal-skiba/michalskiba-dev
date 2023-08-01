from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest

from blog.context import get_home_context, get_post_context
from blog.models import BlogPost
from blog.tests.factories import TagFactory


@pytest.mark.django_db
class TestGetHomeContext:
    def test_correct_blog_posts_fields(self, blog_post: BlogPost) -> None:
        blog_post.release_date = datetime(year=2023, month=5, day=8, tzinfo=timezone.utc)
        blog_post.tags.add(TagFactory(name="tag 1"))
        blog_post.tags.add(TagFactory(name="tag 2"))
        blog_post.save()
        request = Mock()

        context = get_home_context(request)

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

        context = get_home_context(request)

        assert len(context["blog_posts"]) == 2
        assert context["blog_posts"][0]["title"] == blog_post_2.title
        assert context["blog_posts"][1]["title"] == blog_post.title

    def test_not_released_blog_post_included_at_top_for_superuser(
        self, blog_post: BlogPost, blog_post_2: BlogPost
    ) -> None:
        blog_post.release_date = datetime(year=2023, month=5, day=8, tzinfo=timezone.utc)
        blog_post.save()

        request = Mock()

        context = get_home_context(request)

        assert len(context["blog_posts"]) == 2
        assert context["blog_posts"][0]["title"] == blog_post_2.title
        assert context["blog_posts"][1]["title"] == blog_post.title


@pytest.mark.django_db
@patch("blog.context.get_blog_post_html_content", lambda path: "test content")
class TestGetPostContext:
    def test_correct_context(self, blog_post: BlogPost) -> None:
        context = get_post_context(blog_post)

        assert context == {
            "blog_post": {
                "title": blog_post.title,
                "lead": blog_post.lead,
                "tags": blog_post.tags_for_display,
                "html_content": "test content",
                "release_date": blog_post.release_date_for_display,
            }
        }
