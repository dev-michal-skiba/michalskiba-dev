import os
import re
from datetime import datetime, timedelta, timezone

import jwt
from core.api import HttpException, RouteRequest


def get_email(request: RouteRequest) -> str:
    email: str | None = request.body.get("email")
    if not email or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        raise HttpException(status_code=400, detail="Invalid email")
    return email


def get_secure_version_flag(request: RouteRequest) -> bool:
    is_secure_version_on = request.query_paramaters.get("is_secure_version_on") or ""
    return is_secure_version_on.lower() != "false"


def get_host(request: RouteRequest, is_secure_version_on: bool = False) -> str:
    if is_secure_version_on:
        allow_origin = os.environ.get("ALLOW_ORIGIN")
        if not allow_origin:
            raise HttpException(status_code=500, detail="Internal server error")
        return allow_origin
    host: str | None = request.headers.get("x-forwarded-host") or request.headers.get("host")
    if not host:
        raise HttpException(status_code=400, detail="Invalid host header")
    environment = os.environ.get("ENVIRONMENT", "Production").lower()
    protocol = "http" if environment == "local" else "https"

    return f"{protocol}://{host}"


def generate_reset_link(email: str, host: str) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise HttpException(status_code=500, detail="Internal server error")
    token = jwt.encode({"email": email, "exp": expiry.timestamp()}, secret_key, algorithm="HS256")
    return f"{host}/demos/host-header-injection/password-reset/complete/?token={token}"


def extract_token_and_new_password(request: RouteRequest) -> tuple[str, str]:
    token = request.body.get("token")
    new_password = request.body.get("password")
    if not token or not new_password:
        raise HttpException(status_code=400, detail="Please provide token and new password")
    return token, new_password


def validate_token(token: str) -> None:
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise HttpException(status_code=500, detail="Internal server error")
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HttpException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HttpException(status_code=400, detail="Invalid token")


def update_password(token: str, new_password: str) -> None:
    pass
