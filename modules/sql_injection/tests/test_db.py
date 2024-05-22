import pytest
from sql_injection.db import get_parcel_stores


class TestGetParcelStores:
    @pytest.mark.parametrize(
        "is_secure_version_on, expected_parcel_stores",
        (
            (True, []),
            (
                False,
                [
                    {
                        "name": "3.40.1",
                        "address": None,
                        "opening_hours": None,
                    },
                    {
                        "name": "parcel_store_2",
                        "address": "Blue Street 2, 47-404 Wroclaw, Poland",
                        "opening_hours": "7:00-15:00",
                    },
                ],
            ),
        ),
    )
    def test_sql_injection(
        self, is_secure_version_on: bool, expected_parcel_stores: list[dict[str, str]]
    ) -> None:
        parcel_stores = get_parcel_stores(
            address_search_phrase="Wroclaw%' UNION SELECT NULL, sqlite_version(), NULL, NULL, NULL;--",
            is_secure_version_on=is_secure_version_on,
        )

        assert parcel_stores == expected_parcel_stores

    @pytest.mark.parametrize("is_secure_version_on", (True, False))
    def test_normal_query(self, is_secure_version_on: bool) -> None:
        parcel_stores = get_parcel_stores(
            address_search_phrase="Wroclaw",
            is_secure_version_on=is_secure_version_on,
        )

        assert parcel_stores == [
            {
                "name": "parcel_store_2",
                "address": "Blue Street 2, 47-404 Wroclaw, Poland",
                "opening_hours": "7:00-15:00",
            }
        ]
