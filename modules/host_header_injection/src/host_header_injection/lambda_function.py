from typing import Any

from .utils import get_headers


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": 200,
        "body": "ok",
        "headers": get_headers(),
    }
