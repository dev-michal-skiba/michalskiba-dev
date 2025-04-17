import json

import pytest
from auth.lambda_function import lambda_handler


class TestLogin:
    def test_for_valid_credentials(self, victim_access_token: str) -> None:
        event = {
            "body": json.dumps({"username": "victim", "password": "Victim1234!"}),
            "requestContext": {
                "http": {
                    "path": "/api/demo/auth/login",
                    "method": "POST",
                }
            },
        }

        response = lambda_handler(event, context={})

        assert response == {
            "statusCode": 200,
            "headers": {
                "Set-Cookie": f"access_token={victim_access_token}; Secure; HttpOnly; SameSite=Lax; Path=/api/demo",
            },
        }

    def test_for_invalid_credentials(self) -> None:
        event = {
            "body": json.dumps({}),
            "requestContext": {
                "http": {
                    "path": "/api/demo/auth/login",
                    "method": "POST",
                }
            },
        }
        response = lambda_handler(event, context={})

        assert response == {
            "statusCode": 401,
        }


class TestLogout:
    def test(self) -> None:
        event = {
            "requestContext": {
                "http": {
                    "path": "/api/demo/auth/logout",
                    "method": "POST",
                }
            },
        }

        response = lambda_handler(event, context={})

        assert response == {
            "statusCode": 200,
            "headers": {
                "Set-Cookie": "access_token=; Secure; HttpOnly; SameSite=Lax; Path=/api/demo",
            },
        }


class TestAuthorize:
    def test_for_valid_access_token(self, victim_access_token: str) -> None:
        event = {
            "type": "REQUEST",
            "cookies": [f"access_token={victim_access_token}"],
            "requestContext": {
                "http": {
                    "path": "/api/demo/web-parameter-tampering/press-application",
                    "method": "GET",
                }
            },
        }

        response = lambda_handler(event, context={})

        assert response == {"isAuthorized": True, "context": {"username": "victim"}}

    @pytest.mark.parametrize("cookies", (["access_token=test"], []))
    def test_for_invalid_access_token(self, cookies: list[str]) -> None:
        event = {
            "type": "REQUEST",
            "cookies": cookies,
            "requestContext": {
                "http": {
                    "path": "/api/demo/web-parameter-tampering/press-application",
                    "method": "GET",
                }
            },
        }

        response = lambda_handler(event, context={})

        assert response == {"isAuthorized": False}
