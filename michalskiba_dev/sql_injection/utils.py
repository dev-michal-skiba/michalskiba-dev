from django.db.utils import ProgrammingError as DjangoDBUtilsProgrammingError
from psycopg import ProgrammingError as PsycopgProgrammingError

from sql_injection.constants import NON_DATA_QUERY_SQL_COMMANDS
from sql_injection.models import ParcelStore


def get_parcel_stores_from_search_phrase(
    address_search_phrase: str, is_secure_version_on: bool
) -> list[tuple[int, str, str, str]]:
    if is_secure_version_on:
        return _get_parcel_stores_from_search_phrase_securely(address_search_phrase)
    if _is_non_data_query_sql_command_used(address_search_phrase):
        return []
    return _get_parcel_stores_from_search_phrase_insecurely(address_search_phrase)


def _is_non_data_query_sql_command_used(address_search_phrase: str) -> bool:
    address_search_phrase = address_search_phrase.lower()
    for command in NON_DATA_QUERY_SQL_COMMANDS:
        if command in address_search_phrase:
            return True
    return False


def _get_parcel_stores_from_search_phrase_securely(
    address_search_phrase: str,
) -> list[tuple[int, str, str, str]]:
    queryset = ParcelStore.objects.filter(address__contains=address_search_phrase)
    return list(queryset.values_list("id", "name", "address", "opening_hours"))


def _get_parcel_stores_from_search_phrase_insecurely(
    address_search_phrase: str,
) -> list[tuple[int, str, str, str]]:
    query = (
        "SELECT id, name, address, opening_hours FROM sql_injection_parcelstore "
        "WHERE sql_injection_parcelstore.address LIKE '%%{}%%'".format(address_search_phrase)
    )
    try:
        queryset = ParcelStore.objects.raw(query, [])
        return [(store.id, store.name, store.address, store.opening_hours) for store in queryset]
    except (PsycopgProgrammingError, DjangoDBUtilsProgrammingError):
        return []
