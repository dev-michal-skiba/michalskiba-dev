from factory.django import DjangoModelFactory

from blog.models import BlogPostRaw


class BlogPostRawFactory(DjangoModelFactory):
    class Meta:
        model = BlogPostRaw

    content_path = "test_raw_blog_post.md"
