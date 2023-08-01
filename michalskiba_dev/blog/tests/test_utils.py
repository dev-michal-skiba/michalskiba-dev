from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import pytest

from blog.models import BlogPost, BlogPostRaw, Tag
from blog.tests.factories import BlogPostFactory, TagFactory
from blog.utils import (
    convert_blog_post_raw,
    create_blog_post_file,
    get_blog_post_html_content,
    get_or_create_tags,
)


@pytest.mark.django_db
@patch("blog.utils.create_blog_post_file", Mock())
class TestConvertBlogPostRaw:
    def test_blog_post_created(self, blog_post_raw: BlogPostRaw) -> None:
        assert BlogPost.objects.count() == 0

        convert_blog_post_raw(blog_post_raw)

        assert BlogPost.objects.count() == 1
        blog_post = BlogPost.objects.first()
        assert isinstance(blog_post, BlogPost)
        assert blog_post.blog_post_raw == blog_post_raw
        assert blog_post.content_path == "test_blog_post.html"
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

    def test_blog_post_updated(self, blog_post_raw: BlogPostRaw) -> None:
        blog_post = BlogPostFactory(
            blog_post_raw=blog_post_raw,
            content_path="test_path",
            slug="test-title",
            title="Test title",
            lead="Test lead",
        )
        blog_post.tags.add(TagFactory(name="tag 1"))
        blog_post.tags.add(TagFactory(name="tag 2"))
        blog_post.tags.add(TagFactory(name="tag 3"))
        blog_post.tags.add(TagFactory(name="tag 4"))
        assert BlogPost.objects.count() == 1
        assert blog_post.blog_post_raw == blog_post_raw
        assert blog_post.content_path == "test_path"
        assert blog_post.slug == "test-title"
        assert blog_post.title == "Test title"
        assert blog_post.lead == "Test lead"
        assert blog_post.tags.count() == 4

        convert_blog_post_raw(blog_post_raw)

        blog_post.refresh_from_db()
        assert BlogPost.objects.count() == 1
        assert blog_post.blog_post_raw == blog_post_raw
        assert blog_post.content_path == "test_blog_post.html"
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


@patch("blog.utils.settings")
class TestCreateBlogPostFile:
    def test_blog_post_file_created(self, settings_mock: Mock, tmpdir: Any) -> None:
        tmp_file = tmpdir.join(Path("test_blog_post_file_created.html"))
        settings_mock.BLOG_POSTS_PATH = Path(tmp_file.strpath[:-33])
        html_content = "<div>\nHello World!\n</div>"

        create_blog_post_file(
            content_path="test_blog_post_file_created.html", html_content=html_content
        )

        assert tmp_file.read() == html_content


@pytest.mark.django_db
class TestGetOrCreateTags:
    def test_correct_tags_returned_and_created_only_when_did_not_exist(self) -> None:
        TagFactory.create(name="tag 1")
        TagFactory.create(name="tag 3")
        assert Tag.objects.count() == 2

        tags = get_or_create_tags(["tag 1", "tag 2", "tag 3", "tag 4"])

        assert Tag.objects.count() == 4
        assert len(tags) == 4
        tags = list(filter(lambda tag: tag.name, tags))
        assert tags[0].name == "tag 1"
        assert tags[1].name == "tag 2"
        assert tags[2].name == "tag 3"
        assert tags[3].name == "tag 4"


class TestGetBlogPostHtmlContent:
    def test_file_content_returned(self, tmpdir: Any) -> None:
        tmp_file = tmpdir.join(Path("test_file_content_returned.html"))
        with open(tmp_file.strpath, "w") as f:
            f.write("test content")

        content = get_blog_post_html_content(Path(tmp_file.strpath))

        assert content == "test content"
