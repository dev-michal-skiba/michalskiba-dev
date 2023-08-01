from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from blog.context import get_home_context, get_post_context
from blog.models import BlogPost


def home(request: HttpRequest) -> HttpResponse:
    context = get_home_context(request)
    return render(request, "blog/home.html", context)


def about_me(request: HttpRequest) -> HttpResponse:
    return render(request, "blog/about_me.html")


def post(request: HttpRequest, slug: str) -> HttpResponse:
    blog_post = BlogPost.objects.filter_for_display(request.user).filter(slug=slug).first()
    if blog_post is None:
        return redirect("home")
    context = get_post_context(blog_post)
    return render(request, "blog/post.html", context)
