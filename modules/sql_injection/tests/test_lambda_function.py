from unittest import mock

from core.api import LambdaEvent
from core.metrics import MetricName
from sql_injection.lambda_function import lambda_handler


@mock.patch("sql_injection.lambda_function.MetricsClient")
class TestLambdaHandler:
    def test_secure_version(self, mock_metrics_client: mock.Mock) -> None:
        event = LambdaEvent(
            queryStringParameters={"address_search_phrase": "Wroclaw"},
            requestContext={
                "http": {
                    "method": "GET",
                    "path": "/api/demo/sql-injection/parcel-stores",
                }
            },
        )

        response = lambda_handler(event, context={})

        assert response == {
            "statusCode": 200,
            "body": '{"parcel_stores": [{"name": "parcel_store_2", "address": "Blue Street 2, 47-404 Wroclaw, Poland", "opening_hours": "7:00-15:00"}]}',
        }
        assert mock_metrics_client.return_value.log_metric.call_count == 0

    def test_insecure_version(self, mock_metrics_client: mock.Mock) -> None:
        event = LambdaEvent(
            queryStringParameters={
                "address_search_phrase": "abc' UNION SELECT NULL, NULL, NULL, NULL, NULL;--",
                "is_secure_version_on": "false",
            },
            requestContext={
                "http": {
                    "method": "GET",
                    "path": "/api/demo/sql-injection/parcel-stores",
                }
            },
        )

        response = lambda_handler(event, context={})

        assert response == {
            "statusCode": 200,
            "body": '{"parcel_stores": [{"name": null, "address": null, "opening_hours": null}]}',
        }
        assert mock_metrics_client.return_value.log_metric.call_count == 1
        assert mock_metrics_client.return_value.log_metric.call_args[0] == (
            MetricName.SQLI_EXPLOIT,
        )
