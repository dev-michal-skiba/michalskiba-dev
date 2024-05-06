from typing import Any


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": 200,
        "body": "ok",
    }
