from sql_injection.utils import get_address_search_phrase


class TestGetAddressSearchPhrase:
    def test_for_event_with_address_search_phrase_provided(self) -> None:
        address_search_phrase = get_address_search_phrase(
            event={"queryStringParameters": {"address_search_phrase": "Warsaw"}}
        )

        assert address_search_phrase == "Warsaw"

    def test_for_empty_event(self) -> None:
        address_search_phrase = get_address_search_phrase(event={})

        assert address_search_phrase == ""

    def test_for_empty_query_string_parameters(self) -> None:
        address_search_phrase = get_address_search_phrase(event={"queryStringParameters": None})

        assert address_search_phrase == ""
