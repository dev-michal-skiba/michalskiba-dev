import os
from typing import Any


def get_headers(access_token: str) -> dict[str, str]:
    headers = {}
    cookie_template = os.environ.get("COOKIE_TEMPLATE")
    if cookie_template is not None:
        headers["Set-Cookie"] = cookie_template.format(access_token)
    return headers


def get_access_token(event: dict[str, Any]) -> str:
    cookies = event.get("cookies") or []
    access_token_cookie = next(
        filter(
            lambda cookie: cookie.startswith("access_token="),
            cookies,
        ),
        "access_token=",
    )
    return access_token_cookie.split("=", 1)[1]
