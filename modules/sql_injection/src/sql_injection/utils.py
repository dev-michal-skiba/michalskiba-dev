import os
from typing import Any


def extract_query_parameters(event: dict[str, Any]) -> tuple[str, bool]:
    query_string_parameters = event.get("queryStringParameters") or {}
    address_search_phrase = query_string_parameters.get("address_search_phrase") or ""
    is_secure_version_on = query_string_parameters.get("is_secure_version_on") or ""
    is_secure_version_on = is_secure_version_on.lower() != "false"
    return address_search_phrase, is_secure_version_on


def get_headers() -> dict[str, str]:
    allow_origin = os.environ.get("CORS_ALLOW_ORIGIN") or "http://localhost:1313"
    return {
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Credentials": "false",
    }
