import pytest

from demo.models import DemoUser


@pytest.fixture
def victim() -> DemoUser:
    return DemoUser.objects.get(username="victim")
