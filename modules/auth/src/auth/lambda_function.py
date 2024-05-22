import json
from typing import Any

from .domain import User
from .utils import get_access_token, get_headers


def authorize(event: dict[str, Any]) -> dict[str, Any]:
    access_token = get_access_token(event)
    user = User.from_access_token(access_token)
    if user is None:
        return {"isAuthorized": False}
    return {"isAuthorized": True, "context": {"username": user.username}}


def login(event: dict[str, Any]) -> dict[str, Any]:
    body = json.loads(event["body"])
    username = body.get("username") or ""
    password = body.get("password") or ""
    user = User.from_credentials(username, password)
    if user is None:
        return {
            "statusCode": 401,
            "headers": get_headers(),
        }
    return {
        "statusCode": 200,
        "headers": get_headers(access_token=user.access_token),
    }


def logout(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": 200,
        "headers": get_headers(access_token=""),
    }


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    if "type" in event and event["type"] == "REQUEST":
        return authorize(event)
    if event["rawPath"].endswith("/login"):
        return login(event)
    if event["rawPath"].endswith("/logout"):
        return logout(event)
    raise NotImplementedError
