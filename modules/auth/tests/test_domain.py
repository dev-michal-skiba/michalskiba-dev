import pytest
from auth.domain import User


class TestUser:
    class TestGet:
        @pytest.mark.parametrize(
            "username, password", (("victim", "Victim1234!"), ("hacker", "Hacker1234!"))
        )
        def test_correct_credentials(self, username: str, password: str) -> None:
            user = User.get(username, password)

            assert isinstance(user, User)
            assert user.username == username

        @pytest.mark.parametrize("username", ("victim", "hacker", "user"))
        def test_incorrect_credentials(self, username: str) -> None:
            user = User.get(username, "password")

            assert user is None

    class TestAccessToken:
        def test(self) -> None:
            user = User(username="test")

            assert user.access_token == "TEST-ACCESS-TOKEN"
