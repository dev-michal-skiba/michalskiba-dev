import pytest

from blog.models import BlogPostRaw
from blog.raw_parser import get_tags


@pytest.mark.django_db
class TestGetTags:
    def test_correct_tags(self, blog_post_raw: BlogPostRaw) -> None:
        tags = get_tags(file_path=blog_post_raw.absolute_path)

        assert tags == ["tag1", "tag2", "reallylongtagreallylongtag123456"]
