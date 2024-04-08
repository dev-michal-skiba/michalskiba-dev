from datetime import datetime, timedelta, timezone
from typing import Any


def get_address_search_phrase(event: dict[str, Any]) -> str:
    query_string_parameters = event.get("queryStringParameters") or {}
    address_search_phrase = query_string_parameters.get("address_search_phrase") or ""
    return address_search_phrase


def get_is_secure_version_on(event: dict[str, Any]) -> bool:
    headers = event.get("headers") or {}
    cookie_header = headers.get("Cookie") or ""
    if cookie_header:
        cookies = cookie_header.split(";")
        for cookie in cookies:
            cookie = cookie.strip().split("=")
            if len(cookie) == 2 and cookie[0].strip() == "is_secure_version_on":
                cookie_value = cookie[1]
                return cookie_value.lower() == "true"
    return True


def get_headers(is_secure_version_on: bool) -> dict[str, str]:
    expires = (datetime.now(timezone.utc) + timedelta(days=356)).isoformat()
    return {
        "Set-Cookie": f"is_secure_version_on={is_secure_version_on}; Expires={expires}; Path=/; Secure"
    }
