import pytest

from sql_injection.db import get_parcel_stores


class TestGetParcelStores:
    @pytest.mark.parametrize(
        "address_search_phrase, expected_parcel_stores",
        (
            (
                "",
                [
                    {
                        "name": "parcel_store_1",
                        "address": "Red Street 1, 00-001 Warsaw, Poland",
                        "opening_hours": "8:00-18:00",
                        "access_code": "743763",
                    },
                    {
                        "name": "parcel_store_2",
                        "address": "Blue Street 2, 47-404 Wroclaw, Poland",
                        "opening_hours": "7:00-15:00",
                        "access_code": "951620",
                    },
                    {
                        "name": "parcel_store_3",
                        "address": "Green Street 3, 00-001 Warsaw, Poland",
                        "opening_hours": "9:00-17:00",
                        "access_code": "477584",
                    },
                ],
            ),
        ),
    )
    def test_correct_parcel_stores_returned(
        self, address_search_phrase: str, expected_parcel_stores: list[dict[str, str]]
    ) -> None:
        parcel_stores = get_parcel_stores(address_search_phrase, is_secure_version_on=True)

        assert parcel_stores == expected_parcel_stores
