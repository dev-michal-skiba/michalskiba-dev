import json
import os
from typing import Any

from .domain import User


def get_headers(access_token: str | None = None) -> dict[str, str]:
    headers = {
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": os.environ.get("ALLOW_ORIGIN") or "",
    }
    if access_token is not None:
        headers["Set-Cookie"] = f"access_token={access_token}; Secure; HttpOnly; SameSite=Lax"
    return headers


def get_user(event: dict[str, Any]) -> User | None:
    body = json.loads(event["body"])
    username = body.get("username") or ""
    password = body.get("password") or ""
    return User.get(username, password)
