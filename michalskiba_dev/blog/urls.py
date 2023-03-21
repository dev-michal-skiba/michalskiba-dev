from django.urls import path

from .views import about_me, home

urlpatterns = [path("", home, name="home"), path("about-me", about_me, name="about_me")]
