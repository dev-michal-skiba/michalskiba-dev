from web_parameter_tampering.lambda_function import lambda_handler


class TestLambdaHandler:
    def test_lambda_handler(self) -> None:
        response = lambda_handler(event={}, context={})

        assert response == {
            "statusCode": 200,
            "body": "ok",
        }
