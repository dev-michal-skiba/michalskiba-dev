import json
from unittest.mock import Mock, patch

from auth.lambda_function import authorize, lambda_handler, login


@patch("auth.lambda_function.authorize")
@patch("auth.lambda_function.login")
class TestTestLambdaHandler:
    def test_for_login(self, mock_login: Mock, mock_authorize: Mock) -> None:
        expected_response = {"statusCode": 200, "body": "ok"}
        mock_login.return_value = expected_response
        event = {"key": "value"}

        response = lambda_handler(event, context={})

        assert response == expected_response
        mock_login.assert_called_once_with(event)
        mock_authorize.assert_not_called()

    def test_for_authorize(self, mock_login: Mock, mock_authorize: Mock) -> None:
        expected_response = {"statusCode": 200, "body": "ok"}
        mock_authorize.return_value = expected_response
        event = {"type": "REQUEST"}

        response = lambda_handler(event, context={})

        assert response == expected_response
        mock_authorize.assert_called_once_with(event)
        mock_login.assert_not_called()


class TestLogin:
    def test_for_valid_credentials(self) -> None:
        event = {"body": json.dumps({"username": "victim", "password": "Victim1234!"})}

        response = login(event)

        assert response == {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
                "Set-Cookie": "access_token=TEST-ACCESS-TOKEN; Secure; HttpOnly; SameSite=Lax",
            },
        }

    def test_for_invalid_credentials(self) -> None:
        event = {"body": json.dumps({})}

        response = login(event)

        assert response == {
            "statusCode": 401,
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            },
        }


class TestAuthorize:
    def test_for_valid_access_token(self) -> None:
        event = {"type": "REQUEST", "cookies": ["access_token=TEST-ACCESS-TOKEN"]}

        response = authorize(event)

        assert response == {"isAuthorized": True}

    def test_for_invalid_access_token(self) -> None:
        event = {"type": "REQUEST", "cookies": ["access_token=TEST"]}

        response = authorize(event)

        assert response == {"isAuthorized": False}
