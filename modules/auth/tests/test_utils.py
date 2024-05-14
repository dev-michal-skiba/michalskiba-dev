import json
from typing import Any

import pytest
from auth.domain import User
from auth.utils import get_access_token, get_headers, get_user


class TestGetHeaders:
    def test_correct_headers(self) -> None:
        headers = get_headers()

        assert headers == {
            "Access-Control-Allow-Origin": "http://localhost:1313",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Credentials": "true",
        }

    def test_correct_headers_with_access_token(self) -> None:
        headers = get_headers(access_token="token")

        assert headers == {
            "Access-Control-Allow-Origin": "http://localhost:1313",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Credentials": "true",
            "Set-Cookie": "access_token=token; Secure; HttpOnly; SameSite=Lax; Path=/demo",
        }


class TestGetUser:
    def test_correct_user(self) -> None:
        event = {"body": json.dumps({"username": "victim", "password": "Victim1234!"})}

        user = get_user(event)

        assert isinstance(user, User)
        assert user.username == "victim"

    def test_incorrect_user(self) -> None:
        event = {"body": json.dumps({})}

        user = get_user(event)

        assert user is None


class TestGetAccessToken:
    def test_for_existing_access_token(self) -> None:
        event = {"cookies": ["access_token=token"]}

        access_token = get_access_token(event)

        assert access_token == "token"

    @pytest.mark.parametrize("event", (dict(), {"cookies": []}, {"cookies": ["token=a"]}))
    def test_for_not_existing_access_token(self, event: dict[str, Any]) -> None:
        access_token = get_access_token(event)

        assert access_token == ""
