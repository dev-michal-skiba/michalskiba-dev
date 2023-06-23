import pytest
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory

from web_parameter_tampering.constants import IS_SECURE_VERSION_ON_COOKIE_NAME
from web_parameter_tampering.cookies import (
    get_is_secure_version_on,
    set_is_secure_version_on,
)


class TestGetIsSecureVersionOn:
    @pytest.fixture
    def base_request(self) -> HttpRequest:
        return RequestFactory().get("/")

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
