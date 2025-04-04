from web_parameter_tampering.lambda_function import lambda_handler


class TestLambdaHandler:
    def test_for_secure_version(self) -> None:
        response = lambda_handler(
            event={
                "requestContext": {
                    "authorizer": {"lambda": {"username": "hacker"}},
                },
                "queryStringParameters": {"is_secure_version_on": "true", "username": "victim"},
            },
            context={},
        )

        assert response == {
            "statusCode": 200,
            "body": (
                '{"accreditation_code": null, '
                '"organization": "Shady non-existing organization"}'
            ),
        }

    def test_for_insecure_version(self) -> None:
        response = lambda_handler(
            event={
                "requestContext": {
                    "authorizer": {"lambda": {"username": "hacker"}},
                },
                "queryStringParameters": {"is_secure_version_on": "false", "username": "victim"},
            },
            context={},
        )

        assert response == {
            "statusCode": 200,
            "body": (
                '{"accreditation_code": "258c4453-4eff-463d-8169-1d0596fe0b7a", '
                '"organization": "Legitimate organization"}'
            ),
        }
