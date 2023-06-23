from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from web_parameter_tampering.decorators import version


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "web_parameter_tampering/home.html")


def tickets(request: HttpRequest) -> HttpResponse:
    return render(request, "web_parameter_tampering/tickets.html")


@version
def press(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    return render(request, "web_parameter_tampering/press.html")
