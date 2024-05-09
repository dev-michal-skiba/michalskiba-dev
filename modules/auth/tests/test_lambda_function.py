import json

from auth.lambda_function import lambda_handler


class TestLambdaHandler:
    def test_for_valid_credentials(self) -> None:
        event = {"body": json.dumps({"username": "victim", "password": "Victim1234!"})}

        response = lambda_handler(event, context={})

        assert response == {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
                "Set-Cookie": "access_token=; Secure; HttpOnly; SameSite=Lax",
            },
        }

    def test_for_invalid_credentials(self) -> None:
        event = {"body": json.dumps({})}

        response = lambda_handler(event, context={})

        assert response == {
            "statusCode": 401,
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            },
        }
