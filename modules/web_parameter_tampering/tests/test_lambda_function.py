from core.api import LambdaEvent
from web_parameter_tampering.lambda_function import lambda_handler


class TestLambdaHandler:
    def test_for_secure_version(self) -> None:
        event = LambdaEvent(
            requestContext={
                "authorizer": {"lambda": {"username": "hacker"}},
                "http": {
                    "method": "GET",
                    "path": "/api/demo/web-parameter-tampering/press-application",
                },
            },
            queryStringParameters={"is_secure_version_on": "true", "username": "victim"},
        )

        response = lambda_handler(event=event, context={})

        assert response == {
            "statusCode": 200,
            "body": (
                '{"accreditation_code": null, '
                '"organization": "Shady non-existing organization"}'
            ),
        }

    def test_for_insecure_version(self) -> None:
        event = LambdaEvent(
            requestContext={
                "authorizer": {"lambda": {"username": "hacker"}},
                "http": {
                    "method": "GET",
                    "path": "/api/demo/web-parameter-tampering/press-application",
                },
            },
            queryStringParameters={"is_secure_version_on": "false", "username": "victim"},
        )

        response = lambda_handler(event=event, context={})

        assert response == {
            "statusCode": 200,
            "body": (
                '{"accreditation_code": "258c4453-4eff-463d-8169-1d0596fe0b7a", '
                '"organization": "Legitimate organization"}'
            ),
        }

    def test_for_missing_username(self) -> None:
        event = LambdaEvent(
            requestContext={
                "http": {
                    "method": "GET",
                    "path": "/api/demo/web-parameter-tampering/press-application",
                },
            },
        )

        response = lambda_handler(event=event, context={})

        assert response == {
            "statusCode": 404,
            "body": '{"detail": "User not found"}',
        }

    def test_for_non_existing_press_application(self) -> None:
        event = LambdaEvent(
            requestContext={
                "authorizer": {"lambda": {"username": "non-existing-user"}},
                "http": {
                    "method": "GET",
                    "path": "/api/demo/web-parameter-tampering/press-application",
                },
            },
        )

        response = lambda_handler(event=event, context={})

        assert response == {
            "statusCode": 404,
            "body": '{"detail": "Press application not found"}',
        }
