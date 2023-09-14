from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import pytest
from django.contrib.auth.models import User
from django.test import Client

from feature.models import Flag


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
def superuser(superuser_username: str, superuser_email: str, superuser_password: str) -> User:
    return User.objects.create_superuser(superuser_username, superuser_email, superuser_password)


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="test_username", email="test_email@example.com", password="test_password"
    )


@pytest.fixture
def login_superuser(
    superuser: User, superuser_username: str, superuser_password: str
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


@pytest.fixture
def enable_flag() -> Callable[[str], None]:
    def _enable_flag(flag_name: str) -> None:
        Flag.objects.create(name=flag_name, enabled=True)

    return _enable_flag
