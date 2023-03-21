import pytest

from .factories import BlogPostRawFactory


@pytest.fixture
def blog_post_raw() -> BlogPostRawFactory:
    return BlogPostRawFactory()
