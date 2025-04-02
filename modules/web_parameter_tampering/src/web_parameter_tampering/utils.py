from typing import Any


def get_is_secure_version_on(event: dict[str, Any]) -> bool:
    query_string_parameters = event.get("queryStringParameters") or {}
    is_secure_version_on = query_string_parameters.get("is_secure_version_on") or ""
    return is_secure_version_on.lower() != "false"


def get_username(event: dict[str, Any], is_secure_version_on: bool) -> str:
    if is_secure_version_on:
        return event["requestContext"]["authorizer"]["lambda"]["username"]  # type: ignore[no-any-return]
    return event["queryStringParameters"]["username"]  # type: ignore[no-any-return]
