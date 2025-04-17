from core.api import RouteRequest
from web_parameter_tampering.utils import (
    get_is_secure_version_on,
    get_username,
)


class TestGetIsSecureVersionOn:
    def test_is_secure_version_on(self) -> None:
        request = RouteRequest(
            query_paramaters={"is_secure_version_on": "true"},
        )

        is_secure_version_on = get_is_secure_version_on(request)

        assert is_secure_version_on is True

    def test_is_secure_version_off(self) -> None:
        request = RouteRequest(
            query_paramaters={"is_secure_version_on": "false"},
        )

        is_secure_version_on = get_is_secure_version_on(request)

        assert is_secure_version_on is False

    def test_is_secure_version_not_provided(self) -> None:
        request = RouteRequest(
            query_paramaters={},
        )

        is_secure_version_on = get_is_secure_version_on(request)

        assert is_secure_version_on is True


class TestGetUsername:
    def test_is_secure_version_on(self) -> None:
        request = RouteRequest(
            authorizer_username="username_1",
            query_paramaters={"username": "username_2", "is_secure_version_on": "true"},
        )

        username = get_username(request)

        assert username == "username_1"

    def test_is_secure_version_off(self) -> None:
        request = RouteRequest(
            authorizer_username="username_1",
            query_paramaters={"username": "username_2", "is_secure_version_on": "false"},
        )

        username = get_username(request)

        assert username == "username_2"

    def test_username_not_provided(self) -> None:
        request = RouteRequest()

        username = get_username(request)

        assert username is None
