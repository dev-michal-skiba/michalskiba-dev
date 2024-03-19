import os

from peewee import CharField, Model, SqliteDatabase

db = SqliteDatabase(os.environ.get("DB_PATH") or "sql_injection.db")


class BaseModel(Model):
    class Meta:
        database: SqliteDatabase = db


class ParcelStore(BaseModel):
    name: CharField = CharField(max_length=64)
    address: CharField = CharField(max_length=64)
    opening_hours: CharField = CharField(max_length=64)
    access_code: CharField = CharField(max_length=16)


def get_parcel_stores(
    address_search_phrase: str, is_secure_version_on: bool
) -> list[dict[str, str]]:
    queryset = ParcelStore.select().where(ParcelStore.address.contains(address_search_phrase))
    return [
        {
            "name": parcel_store.name,
            "address": parcel_store.address,
            "opening_hours": parcel_store.opening_hours,
            "access_code": parcel_store.access_code,
        }
        for parcel_store in queryset
    ]
