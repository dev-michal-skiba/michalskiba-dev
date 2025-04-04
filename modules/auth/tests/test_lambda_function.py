import json
from unittest.mock import Mock, patch

from auth.lambda_function import authorize, lambda_handler, login, logout


@patch("auth.lambda_function.authorize")
@patch("auth.lambda_function.login")
@patch("auth.lambda_function.logout")
class TestTestLambdaHandler:
    def test_for_login(self, mock_logout: Mock, mock_login: Mock, mock_authorize: Mock) -> None:
        expected_response = {"statusCode": 200, "body": "ok"}
        mock_login.return_value = expected_response
        event = {"rawPath": "/api/demo/auth/login"}

        response = lambda_handler(event, context={})

        assert response == expected_response
        mock_login.assert_called_once_with(event)
        mock_logout.assert_not_called()
        mock_authorize.assert_not_called()

    def test_for_logout(self, mock_logout: Mock, mock_login: Mock, mock_authorize: Mock) -> None:
        expected_response = {"statusCode": 200, "body": "ok"}
        mock_logout.return_value = expected_response
        event = {"rawPath": "/api/demo/auth/logout"}

        response = lambda_handler(event, context={})

        assert response == expected_response
        mock_login.assert_not_called()
        mock_logout.assert_called_once_with(event)
        mock_authorize.assert_not_called()

    def test_for_authorize(
        self, mock_logout: Mock, mock_login: Mock, mock_authorize: Mock
    ) -> None:
        expected_response = {"statusCode": 200, "body": "ok"}
        mock_authorize.return_value = expected_response
        event = {"type": "REQUEST"}

        response = lambda_handler(event, context={})

        assert response == expected_response
        mock_login.assert_not_called()
        mock_logout.assert_not_called()
        mock_authorize.assert_called_once_with(event)


class TestLogin:
    def test_for_valid_credentials(self, victim_access_token: str) -> None:
        event = {"body": json.dumps({"username": "victim", "password": "Victim1234!"})}

        response = login(event)

        assert response == {
            "statusCode": 200,
            "headers": {
                "Set-Cookie": f"access_token={victim_access_token}; Secure; HttpOnly; SameSite=Lax; Path=/api/demo",
            },
        }

    def test_for_invalid_credentials(self) -> None:
        event = {"body": json.dumps({})}

        response = login(event)

        assert response == {
            "statusCode": 401,
        }


class TestLogout:
    def test(self) -> None:
        response = logout(event={})

        assert response == {
            "statusCode": 200,
            "headers": {
                "Set-Cookie": "access_token=; Secure; HttpOnly; SameSite=Lax; Path=/api/demo",
            },
        }


class TestAuthorize:
    def test_for_valid_access_token(self, victim_access_token: str) -> None:
        event = {"type": "REQUEST", "cookies": [f"access_token={victim_access_token}"]}

        response = authorize(event)

        assert response == {"isAuthorized": True, "context": {"username": "victim"}}

    def test_for_invalid_access_token(self) -> None:
        event = {"type": "REQUEST", "cookies": ["access_token=TEST"]}

        response = authorize(event)

        assert response == {"isAuthorized": False}
