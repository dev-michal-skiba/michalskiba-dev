import re
from typing import Callable

import jwt
import pytest
from _pytest.logging import LogCaptureFixture
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.test import RequestFactory
from freezegun import freeze_time

from web_parameter_tampering.constants import (
    AUTH_TOKEN_COOKIE_NAME,
    IS_SECURE_VERSION_ON_COOKIE_NAME,
)
from web_parameter_tampering.cookies import (
    clear_user,
    get_is_secure_version_on,
    get_user,
    set_is_secure_version_on,
    set_user,
)
from web_parameter_tampering.models import User


@pytest.fixture
def base_request() -> HttpRequest:
    return RequestFactory().get("/")


class TestGetIsSecureVersionOn:
    def test_default_value(self, base_request: HttpRequest) -> None:
        is_secure_version_on = get_is_secure_version_on(base_request)

        assert is_secure_version_on is True

    @pytest.mark.parametrize("cookie_value", ("true", "True", "TRUE", "tRuE"))
    def test_when_secure_version_is_set(
        self, base_request: HttpRequest, cookie_value: str
    ) -> None:
        base_request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = cookie_value

        is_secure_version_on = get_is_secure_version_on(base_request)

        assert is_secure_version_on is True

    @pytest.mark.parametrize("cookie_value", ("false", "False", "FALSE", ""))
    def test_when_secure_version_is_not_set(
        self, base_request: HttpRequest, cookie_value: str
    ) -> None:
        base_request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = cookie_value

        is_secure_version_on = get_is_secure_version_on(base_request)

        assert is_secure_version_on is False


class TestSetIsSecureVersionOn:
    @pytest.fixture
    def base_response(self) -> HttpResponse:
        return HttpResponse()

    def test_for_true(self, base_response: HttpResponse) -> None:
        response = set_is_secure_version_on(base_response, value=True)

        cookie_value = str(response.cookies[IS_SECURE_VERSION_ON_COOKIE_NAME])
        assert cookie_value == (
            "Set-Cookie: is_secure_version_on=true; Path=/; SameSite=Lax; Secure"
        )

    def test_for_false(self, base_response: HttpResponse) -> None:
        response = set_is_secure_version_on(base_response, value=False)

        cookie_value = str(response.cookies[IS_SECURE_VERSION_ON_COOKIE_NAME])
        assert cookie_value == (
            "Set-Cookie: is_secure_version_on=false; Path=/; SameSite=Lax; Secure"
        )


@freeze_time("2023-06-27 12:30:00 +0000")
class TestGetUser:
    @pytest.fixture
    def get_request_with_auth_token(
        self, base_request: HttpRequest
    ) -> Callable[[dict[str, str]], HttpRequest]:
        def _get_request_with_auth_token(auth_token_payload: dict[str, str]) -> HttpRequest:
            encoded_user_info = jwt.encode(
                auth_token_payload, settings.SECRET_KEY, algorithm="HS256"
            )
            base_request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = encoded_user_info
            return base_request

        return _get_request_with_auth_token

    def test_none_returned_when_auth_token_is_missing(
        self, base_request: HttpRequest, caplog: LogCaptureFixture
    ) -> None:
        user = get_user(base_request)

        assert user is None
        assert caplog.messages == []

    def test_none_returned_when_auth_token_is_expired(
        self,
        get_request_with_auth_token: Callable[[dict[str, str]], HttpRequest],
        caplog: LogCaptureFixture,
    ) -> None:
        auth_token_payload = {"username": "hacker", "expiry": "2023-06-27 12:29:59 +0000"}
        request = get_request_with_auth_token(auth_token_payload)

        user = get_user(request)

        assert user is None
        assert caplog.messages == []

    def test_none_returned_on_corrupted_auth_token(
        self,
        get_request_with_auth_token: Callable[[dict[str, str]], HttpRequest],
        caplog: LogCaptureFixture,
    ) -> None:
        auth_token_payload = {"username": "hacker", "expiry": "2023-06-28 12:30:00 +0000"}
        request = get_request_with_auth_token(auth_token_payload)
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] += "xyz"

        user = get_user(request)

        assert user is None
        assert caplog.messages == []

    @pytest.mark.parametrize(
        "auth_token_payload", ({"username": "hacker"}, {"expiry": "2023-06-28 12:30:00 +0000"})
    )
    def test_none_returned_on_missing_fields_in_auth_token(
        self,
        get_request_with_auth_token: Callable[[dict[str, str]], HttpRequest],
        auth_token_payload: dict[str, str],
        caplog: LogCaptureFixture,
    ) -> None:
        request = get_request_with_auth_token(auth_token_payload)
        auth_token = request.COOKIES[AUTH_TOKEN_COOKIE_NAME]

        user = get_user(request)

        assert user is None
        assert caplog.messages == [f"Missing required keys in '{auth_token}' auth token"]

    def test_none_returned_on_wrong_expiry_datetime_format(
        self,
        get_request_with_auth_token: Callable[[dict[str, str]], HttpRequest],
        caplog: LogCaptureFixture,
    ) -> None:
        auth_token_payload = {"username": "hacker", "expiry": "2023-06-28 12:30:00"}
        request = get_request_with_auth_token(auth_token_payload)
        auth_token = request.COOKIES[AUTH_TOKEN_COOKIE_NAME]

        user = get_user(request)

        assert user is None
        assert caplog.messages == [f"Failed to get expiry datetime from '{auth_token}' auth token"]

    @pytest.mark.django_db(databases=["web_parameter_tampering"])
    def test_none_returned_when_user_does_not_exist(
        self,
        get_request_with_auth_token: Callable[[dict[str, str]], HttpRequest],
        caplog: LogCaptureFixture,
    ) -> None:
        auth_token_payload = {"username": "bob", "expiry": "2023-06-28 12:30:00 +0000"}
        request = get_request_with_auth_token(auth_token_payload)
        auth_token = request.COOKIES[AUTH_TOKEN_COOKIE_NAME]

        user = get_user(request)

        assert user is None
        assert caplog.messages == [f"Failed to get user from '{auth_token}' auth token"]

    @pytest.mark.django_db(databases=["web_parameter_tampering"])
    def test_user_returned_when_auth_token_valid(
        self,
        get_request_with_auth_token: Callable[[dict[str, str]], HttpRequest],
        caplog: LogCaptureFixture,
    ) -> None:
        auth_token_payload = {"username": "hacker", "expiry": "2023-06-28 12:30:00 +0000"}
        request = get_request_with_auth_token(auth_token_payload)

        user = get_user(request)

        assert isinstance(user, User)
        assert user.username == "hacker"
        assert caplog.messages == []


@pytest.mark.django_db(databases=["web_parameter_tampering"])
@freeze_time("2023-06-20 12:30:00 +0000")
class TestSetUser:
    def test_user_correctly_set_on_response(self, hacker: User) -> None:
        response = HttpResponseRedirect("/")
        assert hasattr(response.cookies, AUTH_TOKEN_COOKIE_NAME) is False

        response = set_user(response, hacker)

        cookie_value = str(response.cookies[AUTH_TOKEN_COOKIE_NAME])
        auth_token_regex = re.compile(
            r"^Set-Cookie: auth_token=(?P<auth_token>.*?); Path=/; SameSite=Lax; Secure$"
        )
        match = auth_token_regex.search(cookie_value)
        assert match
        auth_token = match.group("auth_token")
        auth_token_payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=["HS256"])
        assert auth_token_payload == {"username": "hacker", "expiry": "2023-06-27 12:30:00 +0000"}


class TestClearUser:
    def test_user_correctly_cleared_from_response(self) -> None:
        response = HttpResponseRedirect("/")
        response.set_cookie(
            key=AUTH_TOKEN_COOKIE_NAME,
            value="encoded-auth-token",
            secure=True,
            samesite="Lax",
        )
        assert str(response.cookies[AUTH_TOKEN_COOKIE_NAME]) == (
            "Set-Cookie: auth_token=encoded-auth-token; Path=/; SameSite=Lax; Secure"
        )

        response = clear_user(response)

        assert hasattr(response.cookies, AUTH_TOKEN_COOKIE_NAME) is False

    def test_nothing_happens_when_no_auth_token_to_clear(self) -> None:
        response = HttpResponseRedirect("/")
        assert hasattr(response.cookies, AUTH_TOKEN_COOKIE_NAME) is False

        response = clear_user(response)

        assert hasattr(response.cookies, AUTH_TOKEN_COOKIE_NAME) is False
