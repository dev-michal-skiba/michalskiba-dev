import json
from typing import Any

from .db import get_press_application
from .utils import get_is_secure_version_on, get_username


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    is_secure_version_on = get_is_secure_version_on(event)
    username = get_username(event, is_secure_version_on)
    press_application = get_press_application(username)
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "accreditation_code": press_application.accreditation_code,
                "organization": press_application.organization,
            }
        ),
    }
