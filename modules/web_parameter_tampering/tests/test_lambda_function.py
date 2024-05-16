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
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            },
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
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            },
        }
