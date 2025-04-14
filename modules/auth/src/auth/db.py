from core.db import BaseDatabaseModel, CharField


class User(BaseDatabaseModel):
    username: CharField = CharField(max_length=32, unique=True)
    hashed_password: CharField = CharField()
