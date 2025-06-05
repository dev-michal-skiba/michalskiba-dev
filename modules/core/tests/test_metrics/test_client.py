from unittest import mock

import pytest
from core.api import RouteRequest
from core.metrics import MetricName, MetricsClient, MetricType


@mock.patch("core.logger.logger.uuid4", return_value="uuid")
class TestMetricsClient:
    @pytest.mark.parametrize(
        "api_key, metric_name, expected_user_type",
        [
            ("local-admin-api-key", MetricName.WPT_EXPLOIT, MetricType.ADMIN.value),
            (None, MetricName.WPT_EXPLOIT, MetricType.USER.value),
        ],
    )
    def test_log_metric(
        self,
        mock_uuid4: mock.Mock,
        api_key: str | None,
        metric_name: MetricName,
        expected_user_type: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        route_request = RouteRequest(
            headers={"x-api-key": api_key} if api_key else {},
        )
        monkeypatch.setenv("ADMIN_API_KEY", "local-admin-api-key")
        client = MetricsClient(route_request)

        with mock.patch("builtins.print") as mock_print:
            client.log_metric(metric_name)

        assert mock_print.call_count == 1
        assert (
            mock_print.call_args[0][0]
            == f"[uuid][metrics][{expected_user_type}] {metric_name.value}"
        )
