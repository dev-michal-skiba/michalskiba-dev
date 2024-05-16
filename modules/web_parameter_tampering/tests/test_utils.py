from web_parameter_tampering.utils import (
    get_headers,
    get_is_secure_version_on,
    get_username,
)


class TestGetHeaders:
    def test_correct_headers(self) -> None:
        headers = get_headers()

        assert headers == {
            "Access-Control-Allow-Origin": "http://localhost:1313",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Credentials": "true",
        }


class TestGetIsSecureVersionOn:
    def test_is_secure_version_on(self) -> None:
        is_secure_version_on = get_is_secure_version_on(
            {"queryStringParameters": {"is_secure_version_on": "true"}}
        )

        assert is_secure_version_on is True

    def test_is_secure_version_off(self) -> None:
        is_secure_version_on = get_is_secure_version_on(
            {"queryStringParameters": {"is_secure_version_on": "false"}}
        )

        assert is_secure_version_on is False

    def test_is_secure_version_not_provided(self) -> None:
        is_secure_version_on = get_is_secure_version_on({"queryStringParameters": {}})

        assert is_secure_version_on is True


class TestGetUsername:
    def test_is_secure_version_on(self) -> None:
        event = {
            "requestContext": {
                "authorizer": {"lambda": {"username": "username_1"}},
            },
            "queryStringParameters": {"username": "username_2"},
        }

        username = get_username(event, is_secure_version_on=True)

        assert username == "username_1"

    def test_is_secure_version_off(self) -> None:
        event = {
            "requestContext": {
                "authorizer": {"lambda": {"username": "username_1"}},
            },
            "queryStringParameters": {"username": "username_2"},
        }

        username = get_username(event, is_secure_version_on=False)

        assert username == "username_2"
