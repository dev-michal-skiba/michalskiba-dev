import pytest

from .factories import BlogPostRawFactory


@pytest.mark.django_db
class TestBlogPostRaw:
    def test_is_processed(self, blog_post_raw: BlogPostRawFactory) -> None:
        assert blog_post_raw.is_processed is False
