from django.urls import path

from blog.views import about_me, home, post

urlpatterns = [
    path("", home, name="home"),
    path("about-me", about_me, name="about_me"),
    path(r"post/<str:slug>", post, name="post"),
]
