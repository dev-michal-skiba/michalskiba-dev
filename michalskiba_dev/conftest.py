from typing import Callable

import pytest

from demo.models import DemoUser
from feature.models import Flag


@pytest.fixture
def enable_flag() -> Callable[[str], None]:
    def _enable_flag(flag_name: str) -> None:
        Flag.objects.create(name=flag_name, enabled=True)

    return _enable_flag


@pytest.fixture
def victim() -> DemoUser:
    return DemoUser.objects.get(username="victim")


@pytest.fixture
def hacker() -> DemoUser:
    return DemoUser.objects.get(username="hacker")
