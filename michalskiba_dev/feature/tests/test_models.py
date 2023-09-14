import pytest

from feature.flags import ENABLE_SENTRY_TESTING_ENDPOINT
from feature.models import Flag


@pytest.mark.django_db
class TestFlag:
    def test_str(self) -> None:
        flag = Flag.objects.create(name=ENABLE_SENTRY_TESTING_ENDPOINT)

        assert str(flag) == ENABLE_SENTRY_TESTING_ENDPOINT
