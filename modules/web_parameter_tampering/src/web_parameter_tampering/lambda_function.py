import json
from typing import Any

from .utils import get_headers


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "accreditation_code": "258c4453-4eff-463d-8169-1d0596fe0b7a",
                "organization": "Legitimate organization",
            }
        ),
        "headers": get_headers(),
    }
