import pytest

from web_parameter_tampering.models import PressApplication


@pytest.mark.django_db
class TestPressApplication:
    class TestStr:
        def test_correct_string_returned(self, hacker_press_application: PressApplication) -> None:
            assert str(hacker_press_application) == "Press application <hacker>"
