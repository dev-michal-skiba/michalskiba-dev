from factory.django import DjangoModelFactory

from blog.models import BlogPost, BlogPostRaw, Tag


class BlogPostRawFactory(DjangoModelFactory):
    class Meta:
        model = BlogPostRaw

    content_path = "test_raw_blog_post.md"


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = "tag 1"


class BlogPostFactory(DjangoModelFactory):
    class Meta:
        model = BlogPost

    content_path = "test_blog_post.html"
    title = "Test title"
    slug = "test-slug"
    lead = "Test lead"
