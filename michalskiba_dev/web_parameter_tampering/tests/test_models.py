import pytest

from web_parameter_tampering.models import PressApplication, User


@pytest.mark.django_db
class TestUser:
    class TestLogin:
        def test_returns_none_for_non_existing_user(self) -> None:
            user = User.login("Bob", "password")

            assert user is None

        def test_returns_none_for_incorrect_password(self) -> None:
            user = User.login("hacker", "Hacker1234?")

            assert user is None

        def test_returns_user(self) -> None:
            user = User.login("hacker", "Hacker1234!")

            assert isinstance(user, User)
            assert user.username == "hacker"

    class TestStr:
        def test_correct_string_returned(self, victim: User) -> None:
            assert str(victim) == "victim"


@pytest.mark.django_db
class TestPressApplication:
    class TestStr:
        def test_correct_string_returned(self, hacker_press_application: PressApplication) -> None:
            assert str(hacker_press_application) == "Press application <hacker>"
