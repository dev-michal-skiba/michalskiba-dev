import os

from peewee import CharField, Model, SqliteDatabase

db = SqliteDatabase(os.environ.get("DB_PATH"))


class BaseModel(Model):
    class Meta:
        database: SqliteDatabase = db


class User(BaseModel):
    username: CharField = CharField(max_length=32, unique=True)
    hashed_password: CharField = CharField()
