import os

from peewee import Model, SqliteDatabase

db = SqliteDatabase(os.environ.get("DB_PATH"))


class BaseDatabaseModel(Model):
    class Meta:
        database: SqliteDatabase = db
