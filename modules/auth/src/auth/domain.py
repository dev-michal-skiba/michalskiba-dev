from typing import Self

import bcrypt

from .db import User as UserModel


class User:
    def __init__(self, username: str):
        self.username: str = username
        self.__access_token: str | None = None

    @classmethod
    def get(cls, username: str, password: str) -> Self | None:
        user = UserModel.get_or_none(UserModel.username == username)
        if user is None:
            return None
        is_password_correct = bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8")
        )
        if not is_password_correct:
            return None
        return cls(user.username)

    @property
    def access_token(self) -> str:
        if self.__access_token is None:
            self.__access_token = (
                "TEST-ACCESS-TOKEN"  # TODO Implement proper access token generation
            )
        return self.__access_token
