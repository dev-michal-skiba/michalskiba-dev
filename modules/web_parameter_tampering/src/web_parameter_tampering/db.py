import os

from peewee import CharField, Model, SqliteDatabase

db = SqliteDatabase(os.environ.get("DB_PATH"))


class BaseModel(Model):
    class Meta:
        database: SqliteDatabase = db


class PressApplication(BaseModel):
    username: CharField = CharField(max_length=32, unique=True)
    organization: CharField = CharField(max_length=64)
    accreditation_code: CharField = CharField(max_length=36, null=True)


def get_press_application(username: str) -> PressApplication:
    return PressApplication.get(PressApplication.username == username)  # type: ignore[no-any-return]
