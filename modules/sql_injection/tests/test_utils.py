import pytest

from sql_injection.utils import (
    get_address_search_phrase,
    get_headers,
    get_is_secure_version_on,
)


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


class TestGetIsSecureVersionOn:
    @pytest.mark.parametrize("cookie_value, expected_result", (("True", True), ("false", False)))
    def test_for_event_with_is_secure_version_on_provided(
        self, cookie_value: str, expected_result: bool
    ) -> None:
        is_secure_version_on = get_is_secure_version_on(
            event={"headers": {"Cookie": f"is_secure_version_on={cookie_value}"}}
        )

        assert is_secure_version_on is expected_result

    def test_for_empty_event(self) -> None:
        is_secure_version_on = get_is_secure_version_on(event={})

        assert is_secure_version_on is True

    def test_for_empty_headers(self) -> None:
        is_secure_version_on = get_is_secure_version_on(event={"headers": None})

        assert is_secure_version_on is True

    def test_for_empty_cookie(self) -> None:
        is_secure_version_on = get_is_secure_version_on(event={"headers": {"Cookie": None}})

        assert is_secure_version_on is True

    def test_for_invalid_cookie(self) -> None:
        is_secure_version_on = get_is_secure_version_on(
            event={"headers": {"Cookie": "is_secure_version_onFALSE"}}
        )

        assert is_secure_version_on is True


class TestGetHeaders:
    @pytest.mark.parametrize("is_secure_version_on", (True, False))
    def test_cookie_set_correctly(self, is_secure_version_on: bool, freeze_time: None) -> None:
        headers = get_headers(is_secure_version_on)

        assert headers == {
            "Set-Cookie": (
                f"is_secure_version_on={is_secure_version_on}; "
                f"Expires=2025-03-30T12:00:00+00:00; Path=/; Secure"
            )
        }
