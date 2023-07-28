from pathlib import Path
from typing import Callable
from unittest.mock import patch

import pytest

from blog.models import BlogPost, BlogPostRaw
from blog.post_converter.sections import (
    get_content_html_text,
    get_content_text,
    get_lead_text,
    get_tags,
    get_title_text,
)


@pytest.mark.django_db
class TestGetLeadText:
    def test_correct_lead_text(self, blog_post_raw: BlogPostRaw) -> None:
        lead_text = get_lead_text(file_path=blog_post_raw.absolute_path)

        assert lead_text == "Some xy" + 101 * " lead"


@pytest.mark.django_db
class TestGetTags:
    def test_correct_tags(self, blog_post_raw: BlogPostRaw) -> None:
        tags = get_tags(file_path=blog_post_raw.absolute_path)

        assert tags == ["tag1", "tag2", "reallylongtagreallylongtag123456"]


@pytest.mark.django_db
class TestGetTitleText:
    def test_correct_title_text(self, blog_post_raw: BlogPostRaw) -> None:
        title_text = get_title_text(file_path=blog_post_raw.absolute_path)

        assert title_text == (
            "Some title title title title title title title title title title title title title "
            "title title title title title title title tit"
        )


@pytest.mark.django_db
class TestGetContentText:
    def test_correct_content_text(
        self, blog_post_raw: BlogPostRaw, expected_content_text: str
    ) -> None:
        content_text = get_content_text(file_path=blog_post_raw.absolute_path)

        assert content_text == expected_content_text


@pytest.mark.django_db
@patch("blog.post_converter.converters.static", lambda path: f"/static/{path}")
class TestGetContextHtmlText:
    def test_correct_html_text(
        self,
        assert_file_content: Callable[[Path, str], None],
        blog_post: BlogPost,
        expected_content_text: str,
    ) -> None:
        content_html_text = get_content_html_text(expected_content_text)

        assert_file_content(blog_post.absolute_path, content_html_text)
