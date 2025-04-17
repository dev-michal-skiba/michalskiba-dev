from typing import cast

from core.api import RouteRequest


def get_is_secure_version_on(request: RouteRequest) -> bool:
    is_secure_version_on = request.query_paramaters.get("is_secure_version_on") or ""
    return is_secure_version_on.lower() != "false"


def get_username(request: RouteRequest) -> str | None:
    return (
        request.authorizer_username
        if get_is_secure_version_on(request)
        else cast(str, request.query_paramaters.get("username"))
    )
