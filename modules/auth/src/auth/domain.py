import os
from datetime import datetime, timedelta
from typing import Self

import bcrypt
import jwt
from jwt import PyJWTError

from .db import User as UserModel


class User:
    def __init__(self, username: str):
        self.username: str = username
        self.__access_token: str | None = None

    @classmethod
    def from_credentials(cls, username: str, password: str) -> Self | None:
        user = UserModel.get_or_none(UserModel.username == username)
        if user is None:
            return None
        is_password_correct = bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8")
        )
        if not is_password_correct:
            return None
        return cls(user.username)

    @classmethod
    def from_access_token(cls, access_token: str) -> Self | None:
        try:
            user_info = jwt.decode(access_token, cls.__get_secret_key(), algorithms=["HS256"])
            username = str(user_info["username"])
            expiry = datetime.fromisoformat(user_info["expiry"])
            now = datetime.utcnow()
            if now >= expiry:
                return None
            return cls(username)
        except PyJWTError:
            return None
        except KeyError:
            return None
        except ValueError:
            return None

    @property
    def access_token(self) -> str:
        if self.__access_token is None:
            expiry = datetime.utcnow() + timedelta(days=1)
            token_payload = {
                "username": self.username,
                "expiry": expiry.isoformat(),
            }
            self.__access_token = jwt.encode(
                token_payload, self.__get_secret_key(), algorithm="HS256"
            )
        return self.__access_token

    @classmethod
    def __get_secret_key(cls) -> str:
        secret_key = os.environ.get("SECRET_KEY")
        assert secret_key, "SECRET_KEY environment variable is not set"
        return secret_key
