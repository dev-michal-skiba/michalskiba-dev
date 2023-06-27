from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from web_parameter_tampering.cookies import clear_user, set_user
from web_parameter_tampering.decorators import authentication, version
from web_parameter_tampering.models import PressApplication, User


@authentication
def home(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    user: User | None = kwargs["user"]
    is_logged_in = True if user else False
    return render(request, "web_parameter_tampering/home.html", {"is_logged_in": is_logged_in})


@authentication
def tickets(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    user: User | None = kwargs["user"]
    is_logged_in = True if user else False
    return render(request, "web_parameter_tampering/tickets.html", {"is_logged_in": is_logged_in})


def login(request: HttpRequest) -> HttpResponse:
    response = redirect("/press")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.login(username, password)
        if user:
            response = set_user(response, user)
    return response


@authentication
def logout(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    response = redirect("/press")
    if request.method == "POST":
        user: User | None = kwargs["user"]
        if user:
            response = clear_user(response)
    return response


@version
@authentication
def press(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    is_secure_version_on: bool = kwargs["is_secure_version_on"]
    user: User | None = kwargs["user"]
    if not user:
        return render(request, "web_parameter_tampering/press/login.html")
    if not is_secure_version_on:
        return redirect(f"/press/{user.pk}")
    press_application = get_object_or_404(PressApplication, user=user)
    return render(
        request,
        "web_parameter_tampering/press/press.html",
        {
            "is_logged_in": True,
            "press_application": {
                "organization": press_application.organization,
                "note": press_application.note,
                "accreditation_code": (
                    press_application.accreditation_code if press_application.accepted else ""
                ),
            },
        },
    )


@version
@authentication
def press_insecure(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    is_secure_version_on: bool = kwargs["is_secure_version_on"]
    user: User | None = kwargs["user"]
    if not user or is_secure_version_on:
        return redirect("/press")
    query_user_pk: int = kwargs["user_pk"]
    query_user = get_object_or_404(User, pk=query_user_pk)
    press_application = get_object_or_404(PressApplication, user=query_user)
    return render(
        request,
        "web_parameter_tampering/press/press.html",
        {
            "is_logged_in": True,
            "press_application": {
                "organization": press_application.organization,
                "note": press_application.note,
                "accreditation_code": (
                    press_application.accreditation_code if press_application.accepted else ""
                ),
            },
        },
    )
