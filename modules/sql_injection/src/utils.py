def get_address_search_phrase(event) -> str:
    query_string_parameters = event.get("queryStringParameters") or {}
    address_search_phrase = query_string_parameters.get("address_search_phrase") or ""
    return address_search_phrase
