from typing import Generator

import pytest
from freezegun import freeze_time


@pytest.fixture(autouse=True)
def freeze_time_fixture() -> Generator[None, None, None]:
    with freeze_time("2024-05-16 12:00:00"):
        yield


@pytest.fixture()
def victim_access_token() -> str:
    return (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJ1c2VybmFtZSI6InZpY3RpbSIsImV4cGlyeSI6IjIwMjQtMDUtMTdUMTI6MDA6MDAifQ."
        "qnKGUhBsPbs2YiP6UrxviuquzScRviaLvXDBS2IKn3g"
    )
