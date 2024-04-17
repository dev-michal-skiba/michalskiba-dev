from sql_injection.utils import extract_query_parameters, get_headers


class TestExtractQueryParameters:
    def test_for_event_with_parameters_provided(self) -> None:
        address_search_phrase, is_secure_version_on = extract_query_parameters(
            event={
                "queryStringParameters": {
                    "address_search_phrase": "Warsaw",
                    "is_secure_version_on": "True",
                }
            }
        )

        assert address_search_phrase == "Warsaw"
        assert is_secure_version_on is True

    def test_for_empty_event(self) -> None:
        address_search_phrase, is_secure_version_on = extract_query_parameters(event={})

        assert address_search_phrase == ""
        assert is_secure_version_on is True

    def test_for_empty_query_string_parameters(self) -> None:
        address_search_phrase, is_secure_version_on = extract_query_parameters(
            event={"queryStringParameters": None}
        )

        assert address_search_phrase == ""
        assert is_secure_version_on is True


class TestGetHeaders:
    def test_correct_headers(self) -> None:
        headers = get_headers()

        assert headers == {
            "Access-Control-Allow-Origin": "http://localhost:1313",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Credentials": "false",
        }
