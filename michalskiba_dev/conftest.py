import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import pytest
from django.contrib.auth import get_user_model
from django.test import Client


@pytest.fixture
def test_working_directory() -> Path:
    return Path(os.getcwd())


@pytest.fixture
def assert_file_content() -> Callable[[Path, str], None]:
    def _assert_file_content(file_path: Path, content: str) -> None:
        with open(file_path, "r") as file:
            assert file.read() == content

    return _assert_file_content


@pytest.fixture
def superuser_username() -> str:
    return "admin"


@pytest.fixture
def superuser_email() -> str:
    return "admin@example.com"


@pytest.fixture
def superuser_password() -> str:
    return "password"


@pytest.fixture
def create_superuser(
    superuser_username: str, superuser_email: str, superuser_password: str
) -> None:
    get_user_model().objects.create_superuser(
        superuser_username, superuser_email, superuser_password
    )


@pytest.fixture
@pytest.mark.usefixtures("superuser")
def login_superuser(
    create_superuser: None, superuser_username: str, superuser_password: str
) -> Callable[[Client], None]:
    def _login_superuser(client: Client) -> None:
        client.login(username=superuser_username, password=superuser_password)

    return _login_superuser


@pytest.fixture
def test_datetime() -> datetime:
    return datetime(
        year=2023,
        month=5,
        day=4,
        hour=17,
        minute=44,
        second=17,
        microsecond=345,
        tzinfo=timezone.utc,
    )
