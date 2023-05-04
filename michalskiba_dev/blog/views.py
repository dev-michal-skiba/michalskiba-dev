from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from blog.models import BlogPost


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def about_me(request: HttpRequest) -> HttpResponse:
    return render(request, "about_me.html")


def post(request: HttpRequest, slug: str) -> HttpResponse:
    blog_post = BlogPost.objects.filter_for_display(request.user).filter(slug=slug).first()
    if blog_post is None:
        return redirect("home")
    context = {"blog_post": blog_post}
    return render(request, "post.html", context)
