from pathlib import Path

import pytest

from blog.models import BlogPostRaw
from blog.tests.factories import BlogPostFactory, BlogPostRawFactory


@pytest.fixture
def blog_post_raw(test_working_directory: Path) -> BlogPostRawFactory:
    blog_post_raw = BlogPostRawFactory()
    blog_post_raw.BASE_CONTENT_PATH = test_working_directory / Path("blog/tests/data/raw")
    return blog_post_raw


@pytest.fixture
def blog_post_raw_2(test_working_directory: Path) -> BlogPostRawFactory:
    blog_post_raw = BlogPostRawFactory(content_path="test_raw_blog_post_2.md")
    blog_post_raw.BASE_CONTENT_PATH = test_working_directory / Path("blog/tests/data/raw")
    return blog_post_raw


@pytest.fixture
def blog_post(test_working_directory: Path, blog_post_raw: BlogPostRaw) -> BlogPostFactory:
    blog_post = BlogPostFactory(blog_post_raw=blog_post_raw)
    blog_post.BASE_CONTENT_PATH = test_working_directory / Path("blog/tests/data/posts")
    return blog_post


@pytest.fixture
def blog_post_2(test_working_directory: Path, blog_post_raw_2: BlogPostRaw) -> BlogPostFactory:
    blog_post = BlogPostFactory(
        blog_post_raw=blog_post_raw_2,
        content_path="test_blog_post_2.html",
        title="Title 2",
        slug="title-2",
    )
    blog_post.BASE_CONTENT_PATH = test_working_directory / Path("blog/tests/data/posts")
    return blog_post
