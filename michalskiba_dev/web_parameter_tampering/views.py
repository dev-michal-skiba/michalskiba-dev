from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "web_parameter_tampering/home.html")


def tickets(request: HttpRequest) -> HttpResponse:
    return render(request, "web_parameter_tampering/tickets.html")
