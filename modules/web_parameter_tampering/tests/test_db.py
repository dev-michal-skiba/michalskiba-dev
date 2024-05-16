import pytest
from web_parameter_tampering.db import get_press_application


class TestGetPressApplication:

    @pytest.mark.parametrize(
        "username, expected_organization, expected_accreditation_code",
        (
            ("victim", "Legitimate organization", "258c4453-4eff-463d-8169-1d0596fe0b7a"),
            ("hacker", "Shady non-existing organization", None),
        ),
    )
    def test_get_press_application(
        self, username: str, expected_organization: str, expected_accreditation_code: str | None
    ) -> None:
        press_application = get_press_application(username)

        assert press_application.organization == expected_organization
        assert press_application.accreditation_code == expected_accreditation_code
