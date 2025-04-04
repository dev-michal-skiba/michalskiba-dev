from typing import Any

import pytest
from auth.utils import get_access_token, get_headers


class TestGetHeaders:
    def test_correct_headers(self) -> None:
        headers = get_headers(access_token="token")

        assert headers == {
            "Set-Cookie": "access_token=token; Secure; HttpOnly; SameSite=Lax; Path=/api/demo",
        }


class TestGetAccessToken:
    def test_for_existing_access_token(self) -> None:
        event = {"cookies": ["access_token=token"]}

        access_token = get_access_token(event)

        assert access_token == "token"

    @pytest.mark.parametrize("event", (dict(), {"cookies": []}, {"cookies": ["token=a"]}))
    def test_for_not_existing_access_token(self, event: dict[str, Any]) -> None:
        access_token = get_access_token(event)

        assert access_token == ""
