import pytest

from demo.models import DemoUser


@pytest.mark.django_db
class TestUser:
    class TestLogin:
        def test_returns_none_for_non_existing_user(self) -> None:
            user = DemoUser.login("Bob", "password")

            assert user is None

        def test_returns_none_for_incorrect_password(self) -> None:
            user = DemoUser.login("hacker", "Hacker1234?")

            assert user is None

        def test_returns_user(self) -> None:
            user = DemoUser.login("hacker", "Hacker1234!")

            assert isinstance(user, DemoUser)
            assert user.username == "hacker"

    class TestStr:
        def test_correct_string_returned(self, victim: DemoUser) -> None:
            assert str(victim) == "victim"
