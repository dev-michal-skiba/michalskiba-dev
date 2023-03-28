from django.contrib import admin

from blog.models import BlogPostRaw, Tag

admin.site.register(BlogPostRaw)
admin.site.register(Tag)
