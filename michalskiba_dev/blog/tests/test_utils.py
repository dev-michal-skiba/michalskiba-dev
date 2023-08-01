from pathlib import Path
from typing import Any, Callable
from unittest.mock import Mock, patch

import pytest

from blog.models import BlogPost, BlogPostRaw
from blog.utils import (
    create_blog_post_file,
    get_blog_post_html_content,
    get_extracted_blog_post_info_from_blog_post_raw_file,
)


@pytest.mark.django_db
class TestGetExtractedBlogPostInfoFromBlogPostRawFile:
    def test_extracted_blog_post_info_is_correct(
        self,
        blog_post_raw: BlogPostRaw,
        blog_post: BlogPost,
        assert_file_content: Callable[[Path, str], None],
    ) -> None:
        extracted_blog_post_info = get_extracted_blog_post_info_from_blog_post_raw_file(
            blog_post_raw.absolute_path
        )

        assert extracted_blog_post_info.title == (
            "Some title title title title title title title title title title title title title "
            "title title title title title title title tit"
        )
        assert extracted_blog_post_info.slug == (
            "some-title-title-title-title-title-title-title-title-title-title-title-title-title-"
            "title-title-title-title-title-title-title-tit"
        )
        assert extracted_blog_post_info.lead == "Some xy" + 101 * " lead"
        assert extracted_blog_post_info.tags == [
            "tag1",
            "tag2",
            "reallylongtagreallylongtag123456",
        ]
        assert_file_content(blog_post.absolute_path, extracted_blog_post_info.html_content)


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


class TestGetBlogPostHtmlComntent:
    def test_file_content_returned(self, tmpdir: Any) -> None:
        tmp_file = tmpdir.join(Path("test_file_content_returned.html"))
        with open(tmp_file.strpath, "w") as f:
            f.write("test content")

        content = get_blog_post_html_content(Path(tmp_file.strpath))

        assert content == "test content"
