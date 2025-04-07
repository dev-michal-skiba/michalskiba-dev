from core.api import RouteRequest


def extract_query_parameters(request: RouteRequest) -> tuple[str, bool]:
    address_search_phrase = request.query_paramaters.get("address_search_phrase") or ""
    is_secure_version_on = request.query_paramaters.get("is_secure_version_on") or ""
    is_secure_version_on = is_secure_version_on.lower() != "false"
    return address_search_phrase, is_secure_version_on
