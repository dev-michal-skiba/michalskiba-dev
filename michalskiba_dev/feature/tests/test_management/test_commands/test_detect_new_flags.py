import pytest
from _pytest.logging import LogCaptureFixture
from django.core.management import call_command

from feature.flags import FLAGS
from feature.models import Flag


@pytest.mark.django_db
class TestCommand:
    def test_flags_created(self, caplog: LogCaptureFixture) -> None:
        assert Flag.objects.count() == 0

        call_command("detect_new_flags")

        assert caplog.messages[0] == "Detecting new flags"
        assert caplog.messages[1:] == [f"Added disabled flag '{flag_name}'" for flag_name in FLAGS]
        assert Flag.objects.filter(enabled=False).count() == len(FLAGS)
