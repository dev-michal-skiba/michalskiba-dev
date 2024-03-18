from typing import Any


def get_address_search_phrase(event: dict[str, Any]) -> str:
    query_string_parameters = event.get("queryStringParameters") or {}
    address_search_phrase = query_string_parameters.get("address_search_phrase") or ""
    return address_search_phrase
