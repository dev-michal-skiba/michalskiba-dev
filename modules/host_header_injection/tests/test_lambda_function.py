from host_header_injection.lambda_function import lambda_handler


class TestLambdaHandler:
    def test_lambda_handler(self) -> None:
        response = lambda_handler(event={}, context={})

        assert response == {
            "statusCode": 200,
            "body": "ok",
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            },
        }
