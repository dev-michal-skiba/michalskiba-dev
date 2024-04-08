import json
from typing import Any

from db import get_parcel_stores
from utils import get_address_search_phrase, get_headers, get_is_secure_version_on


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    is_secure_version_on = get_is_secure_version_on(event)
    parcel_stores = get_parcel_stores(
        address_search_phrase=get_address_search_phrase(event),
        is_secure_version_on=is_secure_version_on,
    )
    return {
        "statusCode": 200,
        "body": json.dumps(parcel_stores),
        "headers": get_headers(is_secure_version_on),
    }
