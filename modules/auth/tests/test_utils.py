import json

from auth.domain import User
from auth.utils import get_headers, get_user


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
            "Set-Cookie": "access_token=token; Secure; HttpOnly; SameSite=Lax",
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
