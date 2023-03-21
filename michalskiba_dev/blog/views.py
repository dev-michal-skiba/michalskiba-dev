from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def about_me(request: HttpRequest) -> HttpResponse:
    return render(request, "about_me.html")
