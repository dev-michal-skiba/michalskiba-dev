from lib.peewee import CharField, Model, SqliteDatabase

db = SqliteDatabase("sql_injection.db")


class BaseModel(Model):
    class Meta:
        database = db


class ParcelStore(BaseModel):
    name = CharField(max_length=64)
    address = CharField(max_length=64)
    opening_hours = CharField(max_length=64)
    access_code = CharField(max_length=16)


def get_parcel_stores(
    address_search_phrase: str, is_secure_version_on: bool
) -> list[dict[str, str]]:
    return [
        {
            "name": parcel_store.name,
            "address": parcel_store.address,
            "opening_hours": parcel_store.opening_hours,
            "access_code": parcel_store.access_code,
        }
        for parcel_store in ParcelStore.select()
    ]
