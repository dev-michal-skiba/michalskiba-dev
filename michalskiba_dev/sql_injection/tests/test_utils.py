from unittest.mock import Mock, patch

import pytest

from sql_injection.utils import (
    _get_parcel_stores_from_search_phrase_insecurely,
    _get_parcel_stores_from_search_phrase_securely,
    get_parcel_stores_from_search_phrase,
)


@patch("sql_injection.utils._get_parcel_stores_from_search_phrase_securely")
@patch("sql_injection.utils._get_parcel_stores_from_search_phrase_insecurely")
class TestGetParcelStoresFromSearchPhrase:
    def test_secure_version_used_when_secure_version_is_on(
        self, mock_insecure_version: Mock, mock_secure_version: Mock
    ) -> None:
        get_parcel_stores_from_search_phrase(address_search_phrase="", is_secure_version_on=True)

        assert mock_insecure_version.call_count == 0
        assert mock_secure_version.call_count == 1

    def test_insecure_version_used_when_secure_version_is_off(
        self, mock_insecure_version: Mock, mock_secure_version: Mock
    ) -> None:
        get_parcel_stores_from_search_phrase(address_search_phrase="", is_secure_version_on=False)

        assert mock_insecure_version.call_count == 1
        assert mock_secure_version.call_count == 0


@pytest.mark.django_db(databases=["sql_injection"])
class TestGetParcelStoresFromSearchPhraseSecurely:
    def test_parcel_stores_returned_correctly(self) -> None:
        parcel_stores = _get_parcel_stores_from_search_phrase_securely("Warsaw")

        assert parcel_stores == [
            (1, "parcel_store_1", "Red Street 1, 00-001 Warsaw, Poland", "8:00-18:00"),
            (3, "parcel_store_3", "Green Street 3, 00-001 Warsaw, Poland", "9:00-17:00"),
        ]

    def test_injection_does_not_work(self) -> None:
        parcel_stores = _get_parcel_stores_from_search_phrase_securely(
            "Warsaw%%' UNION SELECT NULL, name, address, access_code "
            "FROM sql_injection_parcelstore; --"
        )

        assert parcel_stores == []


@pytest.mark.django_db(databases=["sql_injection"])
class TestGetParcelStoresFromSearchPhraseInsecurely:
    def test_parcel_stores_returned_correctly(self) -> None:
        parcel_stores = _get_parcel_stores_from_search_phrase_insecurely("Warsaw")

        assert parcel_stores == [
            (1, "parcel_store_1", "Red Street 1, 00-001 Warsaw, Poland", "8:00-18:00"),
            (3, "parcel_store_3", "Green Street 3, 00-001 Warsaw, Poland", "9:00-17:00"),
        ]

    def test_injection_works(self) -> None:
        parcel_stores = _get_parcel_stores_from_search_phrase_insecurely(
            "Poznan%%' UNION SELECT id, name, address, access_code "
            "FROM sql_injection_parcelstore; --"
        )

        assert parcel_stores == [
            (1, "parcel_store_1", "Red Street 1, 00-001 Warsaw, Poland", "743763"),
            (2, "parcel_store_2", "Blue Street 2, 47-404 Wroclaw, Poland", "951620"),
            (3, "parcel_store_3", "Green Street 3, 00-001 Warsaw, Poland", "477584"),
        ]
