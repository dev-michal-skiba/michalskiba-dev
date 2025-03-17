import json
from typing import Any

from .exception import HTTPException
from .utils import (
    extract_token_and_new_password,
    generate_reset_link,
    get_email,
    get_headers,
    get_host,
    get_secure_version_flag,
    update_password,
    validate_token,
)


def initiate_password_reset(event: dict[str, Any]) -> dict[str, Any]:
    email = get_email(event)
    is_secure_version_on = get_secure_version_flag(event)
    host = get_host(event, is_secure_version_on)
    reset_link = generate_reset_link(email, host)
    return {
        "statusCode": 200,
        "body": json.dumps({"reset_link": reset_link}),
        "headers": get_headers(),
    }


def complete_password_reset(event: dict[str, Any]) -> dict[str, Any]:
    token, new_password = extract_token_and_new_password(event)
    validate_token(token)
    update_password(token, new_password)
    return {
        "statusCode": 204,
        "headers": get_headers(),
        "body": "",
    }


def preflight() -> dict[str, Any]:
    return {
        "statusCode": 200,
        "body": "",
        "headers": get_headers(),
    }


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    try:
        http_method = event.get("requestContext", {}).get("http", {}).get("method")
        if http_method == "OPTIONS":
            return preflight()
        if http_method == "POST":
            if event["rawPath"].endswith("/password-reset/initiate"):
                return initiate_password_reset(event)
            if event["rawPath"].endswith("/password-reset/complete"):
                return complete_password_reset(event)
            raise HTTPException(404, "Not Found")
        raise HTTPException(405, "Method Not Allowed")
    except HTTPException as e:
        return {
            "statusCode": e.status_code,
            "body": json.dumps({"detail": e.detail}),
            "headers": get_headers(),
        }
