from typing import Any

from .utils import get_access_token, get_headers, get_user


def authorize(event: dict[str, Any]) -> dict[str, bool]:
    access_token = get_access_token(event)
    is_authorized = access_token == "TEST-ACCESS-TOKEN"  # TODO Implement proper access token check
    return {"isAuthorized": is_authorized}


def login(event: dict[str, Any]) -> dict[str, Any]:
    user = get_user(event)
    if user is None:
        return {
            "statusCode": 401,
            "headers": get_headers(),
        }
    return {
        "statusCode": 200,
        "headers": get_headers(user.access_token),
    }


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    if "type" in event and event["type"] == "REQUEST":
        return authorize(event)
    return login(event)
