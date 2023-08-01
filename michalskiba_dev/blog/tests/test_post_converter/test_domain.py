from pathlib import Path
from typing import Callable

import pytest

from blog.models import BlogPost, BlogPostRaw
from blog.post_converter import get_extracted_blog_post_from_blog_post_raw_file


@pytest.mark.django_db
class TestGetExtractedBlogPostFromBlogPostRawFile:
    def test_extracted_blog_post_info_is_correct(
        self,
        blog_post_raw: BlogPostRaw,
        blog_post: BlogPost,
        assert_file_content: Callable[[Path, str], None],
    ) -> None:
        extracted_blog_post_info = get_extracted_blog_post_from_blog_post_raw_file(
            blog_post_raw.absolute_path
        )

        assert extracted_blog_post_info.content_path == "test_blog_post.html"
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
