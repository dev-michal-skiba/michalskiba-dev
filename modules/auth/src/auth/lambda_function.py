from typing import Any

from .utils import get_headers, get_user


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
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
