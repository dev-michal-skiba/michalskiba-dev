from pathlib import Path

import pytest

from blog.tests.factories import BlogPostRawFactory


@pytest.fixture
def blog_post_raw(test_working_directory: Path) -> BlogPostRawFactory:
    blog_post_raw = BlogPostRawFactory()
    blog_post_raw.BASE_CONTENT_PATH = test_working_directory / Path("blog/tests/data/raw")
    return blog_post_raw
