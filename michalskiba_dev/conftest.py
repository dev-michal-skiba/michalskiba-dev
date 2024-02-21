import pytest

from demo.models import DemoUser


@pytest.fixture
def victim() -> DemoUser:
    return DemoUser.objects.get(username="victim")


@pytest.fixture
def hacker() -> DemoUser:
    return DemoUser.objects.get(username="hacker")
