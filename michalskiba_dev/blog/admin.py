from django.contrib import admin

from blog.models import BlogPost, BlogPostRaw, Tag

admin.site.register(BlogPostRaw)
admin.site.register(Tag)
admin.site.register(BlogPost)
