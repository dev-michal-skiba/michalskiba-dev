from factory.django import DjangoModelFactory

from blog.models import BlogPost, BlogPostRaw


class BlogPostRawFactory(DjangoModelFactory):
    class Meta:
        model = BlogPostRaw

    content_path = "test_raw_blog_post.md"


class BlogPostFactory(DjangoModelFactory):
    class Meta:
        model = BlogPost

    content_path = "test_blog_post.html"
