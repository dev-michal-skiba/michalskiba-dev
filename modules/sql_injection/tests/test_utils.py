from core.api import RouteRequest
from sql_injection.utils import extract_query_parameters


class TestExtractQueryParameters:
    def test_with_query_parameters(self) -> None:
        request = RouteRequest(
            query_paramaters={"address_search_phrase": "Warsaw", "is_secure_version_on": "True"}
        )

        address_search_phrase, is_secure_version_on = extract_query_parameters(request)

        assert address_search_phrase == "Warsaw"
        assert is_secure_version_on is True

    def test_without_query_parameters(self) -> None:
        request = RouteRequest(query_paramaters={})

        address_search_phrase, is_secure_version_on = extract_query_parameters(request)

        assert address_search_phrase == ""
        assert is_secure_version_on is True
