from unittest.mock import Mock

import pytest
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory

from web_parameter_tampering.constants import IS_SECURE_VERSION_ON_COOKIE_NAME
from web_parameter_tampering.decorators import version


class TestVersion:
    @pytest.fixture
    def base_request(self) -> HttpRequest:
        return RequestFactory().get("/")

    @pytest.fixture
    def base_response(self) -> HttpResponse:
        return HttpResponse()

    def test_when_secure_version_is_defaulted(
        self, base_request: HttpRequest, base_response: HttpResponse
    ) -> None:
        view_mock = Mock()
        view_mock.return_value = base_response

        response = version(view_mock)(base_request, *[], **{})

        view_mock.assert_called_once_with(base_request, is_secure_version_on=True)
        cookie_value = str(response.cookies[IS_SECURE_VERSION_ON_COOKIE_NAME])
        assert cookie_value == (
            "Set-Cookie: is_secure_version_on=true; Path=/; SameSite=Lax; Secure"
        )

    def test_when_secure_version_is_set(
        self, base_request: HttpRequest, base_response: HttpResponse
    ) -> None:
        view_mock = Mock()
        view_mock.return_value = base_response
        base_request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = "true"

        response = version(view_mock)(base_request, *[], **{})

        view_mock.assert_called_once_with(base_request, is_secure_version_on=True)
        cookie_value = str(response.cookies[IS_SECURE_VERSION_ON_COOKIE_NAME])
        assert cookie_value == (
            "Set-Cookie: is_secure_version_on=true; Path=/; SameSite=Lax; Secure"
        )

    def test_when_secure_version_is_not_set(
        self, base_request: HttpRequest, base_response: HttpResponse
    ) -> None:
        view_mock = Mock()
        view_mock.return_value = base_response
        base_request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = "false"

        response = version(view_mock)(base_request, *[], **{})

        view_mock.assert_called_once_with(base_request, is_secure_version_on=False)
        cookie_value = str(response.cookies[IS_SECURE_VERSION_ON_COOKIE_NAME])
        assert cookie_value == (
            "Set-Cookie: is_secure_version_on=false; Path=/; SameSite=Lax; Secure"
        )
