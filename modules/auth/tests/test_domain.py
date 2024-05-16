import pytest
from auth.domain import User


class TestUser:
    class TestFromCredentials:
        @pytest.mark.parametrize(
            "username, password", (("victim", "Victim1234!"), ("hacker", "Hacker1234!"))
        )
        def test_correct_credentials(self, username: str, password: str) -> None:
            user = User.from_credentials(username, password)

            assert isinstance(user, User)
            assert user.username == username

        @pytest.mark.parametrize("username", ("victim", "hacker", "user"))
        def test_incorrect_credentials(self, username: str) -> None:
            user = User.from_credentials(username, "password")

            assert user is None

    class TestFromAccessToken:
        def test_for_valid_access_token(self, victim_access_token: str) -> None:
            user = User.from_access_token(victim_access_token)

            assert isinstance(user, User)
            assert user.username == "victim"

    class TestAccessToken:
        def test(self, victim_access_token: str) -> None:
            user = User(username="victim")

            assert user.access_token == victim_access_token
