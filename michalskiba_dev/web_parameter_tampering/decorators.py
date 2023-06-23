from typing import Any, Callable

from django.http import HttpRequest, HttpResponse

from web_parameter_tampering.cookies import (
    get_is_secure_version_on,
    set_is_secure_version_on,
)


def version(
    view: Callable[[HttpRequest, Any, Any], HttpResponse]
) -> Callable[[HttpRequest, Any, Any], HttpResponse]:
    def _view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        is_secure_version_on = get_is_secure_version_on(request)
        kwargs["is_secure_version_on"] = is_secure_version_on
        response = view(request, *args, **kwargs)
        response = set_is_secure_version_on(response, is_secure_version_on)
        return response

    return _view
