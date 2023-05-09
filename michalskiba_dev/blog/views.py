from typing import Any

from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from blog.models import BlogPost
from blog.utils import get_blog_post_html_content


def _get_home_context(request: HttpRequest) -> dict[str, Any]:
    return {
        "blog_posts": [
            {
                "title": blog_post.title,
                "release_date": blog_post.release_date_for_display,
                "tags": blog_post.tags_for_display,
                "link": reverse("post", kwargs={"slug": blog_post.slug}),
                "lead": blog_post.lead,
            }
            for blog_post in BlogPost.objects.filter_for_display(request.user).order_by(
                F("release_date").desc(nulls_first=True)
            )
        ]
    }


def home(request: HttpRequest) -> HttpResponse:
    context = _get_home_context(request)
    return render(request, "home.html", context)


def about_me(request: HttpRequest) -> HttpResponse:
    return render(request, "about_me.html")


def _get_post_context(blog_post: BlogPost) -> dict[str, Any]:
    return {
        "blog_post": {
            "title": blog_post.title,
            "lead": blog_post.lead,
            "tags": blog_post.tags_for_display,
            "html_content": get_blog_post_html_content(blog_post.absolute_path),
            "release_date": blog_post.release_date_for_display,
        }
    }


def post(request: HttpRequest, slug: str) -> HttpResponse:
    blog_post = BlogPost.objects.filter_for_display(request.user).filter(slug=slug).first()
    if blog_post is None:
        return redirect("home")
    context = _get_post_context(blog_post)
    return render(request, "post.html", context)
