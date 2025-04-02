import json
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from .exception import HTTPException


def get_email(event: dict[str, Any]) -> str:
    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON body")
    email: str | None = body.get("email")
    if not email or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        raise HTTPException(400, "Invalid email")
    return email


def get_secure_version_flag(event: dict[str, Any]) -> bool:
    query_string_parameters = event.get("queryStringParameters") or {}
    is_secure_version_on = query_string_parameters.get("is_secure_version_on") or ""
    return is_secure_version_on.lower() != "false"


def get_host(event: dict[str, Any], is_secure_version_on: bool = False) -> str:
    if is_secure_version_on:
        allow_origin = os.environ.get("ALLOW_ORIGIN")
        if not allow_origin:
            raise HTTPException(500, "Internal server error")
        return allow_origin
    headers = event.get("headers", {})
    headers = {k.lower(): v for k, v in headers.items()}
    host: str | None = headers.get("x-forwarded-host") or headers.get("host")
    if not host:
        raise HTTPException(400, "Invalid host header")
    environment = os.environ.get("ENVIRONMENT", "Production").lower()
    protocol = "http" if environment == "local" else "https"

    return f"{protocol}://{host}"


def generate_reset_link(email: str, host: str) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise HTTPException(500, "Internal server error")
    token = jwt.encode({"email": email, "exp": expiry.timestamp()}, secret_key, algorithm="HS256")
    return f"{host}/demos/host-header-injection/password-reset/complete/?token={token}"


def extract_token_and_new_password(event: dict[str, Any]) -> tuple[str, str]:
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON body")
    token = body.get("token")
    new_password = body.get("password")
    if not token or not new_password:
        raise HTTPException(400, "Please provide token and new password")
    return token, new_password


def validate_token(token: str) -> None:
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise HTTPException(500, "Internal server error")
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(400, "Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(400, "Invalid token")


def update_password(token: str, new_password: str) -> None:
    pass
