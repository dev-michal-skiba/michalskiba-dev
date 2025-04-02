import json
from typing import Any

from .db import get_parcel_stores
from .utils import extract_query_parameters


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    address_search_phrase, is_secure_version_on = extract_query_parameters(event)
    parcel_stores = get_parcel_stores(
        address_search_phrase=address_search_phrase,
        is_secure_version_on=is_secure_version_on,
    )
    return {
        "statusCode": 200,
        "body": json.dumps(parcel_stores),
    }
