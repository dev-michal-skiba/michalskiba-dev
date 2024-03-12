import json

from db import get_parcel_stores


def lambda_handler(event, context):
    parcel_stores = get_parcel_stores(
        address_search_phrase="", is_secure_version_on=True
    )
    return {"statusCode": 200, "body": json.dumps(parcel_stores)}
