import pytest
from _pytest.logging import LogCaptureFixture

from feature.flags import ENABLE_SENTRY_TESTING_ENDPOINT, FLAGS, is_flag_enabled
from feature.models import Flag


class TestFlags:
    @pytest.mark.parametrize("flag_name", FLAGS)
    def test_flags_length(self, flag_name: str) -> None:
        assert len(flag_name) <= 64


@pytest.mark.django_db
class TestIsFlagEnabled:
    def test_for_unknown_flag_name(self) -> None:
        assert is_flag_enabled("xyz") is False

    @pytest.mark.parametrize("enabled, expected_enabled", ((False, False), (True, True)))
    def test_for_existing_flag(self, enabled: bool, expected_enabled: bool) -> None:
        Flag.objects.create(name=ENABLE_SENTRY_TESTING_ENDPOINT, enabled=enabled)

        assert is_flag_enabled(ENABLE_SENTRY_TESTING_ENDPOINT) is expected_enabled

    def test_for_non_existing_flag(self, caplog: LogCaptureFixture) -> None:
        enabled = is_flag_enabled(ENABLE_SENTRY_TESTING_ENDPOINT)

        assert caplog.messages == [
            f"Tried to check non existing flag '{ENABLE_SENTRY_TESTING_ENDPOINT}'"
        ]
        assert enabled is False
