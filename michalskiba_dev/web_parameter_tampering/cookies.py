from django.http import HttpRequest, HttpResponse

from web_parameter_tampering.constants import IS_SECURE_VERSION_ON_COOKIE_NAME


def get_is_secure_version_on(request: HttpRequest) -> bool:
    value = request.COOKIES.get(IS_SECURE_VERSION_ON_COOKIE_NAME, "true")
    return value.lower() == "true"


def set_is_secure_version_on(response: HttpResponse, value: bool) -> HttpResponse:
    raw_value = "true" if value else "false"
    response.set_cookie(
        key=IS_SECURE_VERSION_ON_COOKIE_NAME,
        value=raw_value,
        secure=True,
        samesite="Lax",
    )
    return response
