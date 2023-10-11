from unittest.mock import Mock, patch

import pytest

from sql_injection.utils import (
    _get_parcel_stores_from_search_phrase_insecurely,
    _get_parcel_stores_from_search_phrase_securely,
    _is_non_data_query_sql_command_used,
    get_parcel_stores_from_search_phrase,
)


@patch("sql_injection.utils._get_parcel_stores_from_search_phrase_securely")
@patch("sql_injection.utils._get_parcel_stores_from_search_phrase_insecurely")
class TestGetParcelStoresFromSearchPhrase:
    def test_secure_version_used_when_secure_version_is_on(
        self, mock_insecure_version: Mock, mock_secure_version: Mock
    ) -> None:
        get_parcel_stores_from_search_phrase(
            address_search_phrase="CREATE TABLE person (name varchar(255));",
            is_secure_version_on=True,
        )

        assert mock_insecure_version.call_count == 0
        assert mock_secure_version.call_count == 1

    def test_insecure_version_used_when_secure_version_is_off(
        self, mock_insecure_version: Mock, mock_secure_version: Mock
    ) -> None:
        get_parcel_stores_from_search_phrase(address_search_phrase="", is_secure_version_on=False)

        assert mock_insecure_version.call_count == 1
        assert mock_secure_version.call_count == 0

    def test_empty_list_returned_when_insecure_version_used_with_non_data_query_sql_statement(
        self, mock_insecure_version: Mock, mock_secure_version: Mock
    ) -> None:
        parcel_stores = get_parcel_stores_from_search_phrase(
            address_search_phrase="CREATE TABLE person (name varchar(255));",
            is_secure_version_on=False,
        )

        assert parcel_stores == []
        assert mock_insecure_version.call_count == 0
        assert mock_secure_version.call_count == 0


class TestIsNonDataQuerySqlCommandUsed:
    def test_returns_false_for_data_query_sql_statement(self) -> None:
        is_non_data_query_sql_command_used = _is_non_data_query_sql_command_used(
            "Warsaw%%' UNION SELECT NULL, name, address, access_code "
            "FROM sql_injection_parcelstore; --"
        )

        assert is_non_data_query_sql_command_used is False

    @pytest.mark.parametrize(
        "statement",
        (
            "CREATE TABLE person (name varchar(255));",
            "DROP TABLE person;",
            "ALTER TABLE person",
            "TRUNCATE TABLE person;",
            "INSERT INTO person (column1, column2) VALUES (1, 2);",
            "UPDATE table_name SET column1 = value1 WHERE condition;",
            "DELETE FROM table_name WHERE condition;",
            "CALL do_db_maintenance();",
            "LOCK TABLE films IN SHARE MODE;",
            "COMMIT;",
            "SAVEPOINT my_savepoint;",
            "ROLLBACK;",
            "table_name SET column1 = value1 WHERE condition;",
            "GRANT admins TO joe;",
            "REVOKE admins FROM joe;",
        ),
    )
    def test_returns_true_for_non_data_query_sql_statement(self, statement: str) -> None:
        is_non_data_query_sql_command_used = _is_non_data_query_sql_command_used(statement)

        assert is_non_data_query_sql_command_used is True


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

    def test_empty_list_returned_on_invalid_injection(self) -> None:
        parcel_stores = _get_parcel_stores_from_search_phrase_insecurely(
            "Warsaw%%'; INSERT INTO sql_injection_parcelstore (name, address, opening_hours, "
            "access_code) VALUES ('a', 'b', 'c', 'd') RETURNING id, address, name, dummy; --"
        )

        assert parcel_stores == []
