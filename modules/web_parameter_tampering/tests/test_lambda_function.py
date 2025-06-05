from unittest import mock

from core.api import LambdaEvent
from core.metrics import MetricName
from web_parameter_tampering.lambda_function import lambda_handler


@mock.patch("web_parameter_tampering.lambda_function.MetricsClient")
class TestLambdaHandler:
    def test_for_secure_version(self, mock_metrics_client: mock.Mock) -> None:
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
        assert mock_metrics_client.return_value.log_metric.call_count == 0

    def test_for_insecure_version(self, mock_metrics_client: mock.Mock) -> None:
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
        assert mock_metrics_client.return_value.log_metric.call_count == 1
        assert mock_metrics_client.return_value.log_metric.call_args[0] == (
            MetricName.WPT_EXPLOIT,
        )

    def test_for_missing_username(self, mock_metrics_client: mock.Mock) -> None:
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
        assert mock_metrics_client.return_value.log_metric.call_count == 0

    def test_for_non_existing_press_application(self, mock_metrics_client: mock.Mock) -> None:
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
