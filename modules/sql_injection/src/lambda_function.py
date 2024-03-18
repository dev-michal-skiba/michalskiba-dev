import json

from db import get_parcel_stores
from utils import get_address_search_phrase


def lambda_handler(event, context):
    parcel_stores = get_parcel_stores(
        address_search_phrase=get_address_search_phrase(event),
        is_secure_version_on=True,
    )
    return {"statusCode": 200, "body": json.dumps(parcel_stores)}
