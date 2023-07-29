import pytest

from blog.models import BlogPostRaw
from blog.tests.factories import BlogPostFactory, BlogPostRawFactory, TagFactory


@pytest.fixture
def blog_post_raw() -> BlogPostRawFactory:
    blog_post_raw = BlogPostRawFactory()
    return blog_post_raw


@pytest.fixture
def blog_post_raw_2() -> BlogPostRawFactory:
    blog_post_raw = BlogPostRawFactory(content_path="test_blog_post_2.md")
    return blog_post_raw


@pytest.fixture
def blog_post(blog_post_raw: BlogPostRaw) -> BlogPostFactory:
    blog_post = BlogPostFactory(blog_post_raw=blog_post_raw)
    return blog_post


@pytest.fixture
def blog_post_2(blog_post_raw_2: BlogPostRaw) -> BlogPostFactory:
    blog_post = BlogPostFactory(
        blog_post_raw=blog_post_raw_2,
        content_path="test_blog_post_2.html",
        title="Title 2",
        slug="title-2",
    )
    return blog_post


@pytest.fixture
def tag() -> TagFactory:
    return TagFactory(name="test tag")
