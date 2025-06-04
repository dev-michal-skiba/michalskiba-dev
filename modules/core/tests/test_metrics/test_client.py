from unittest import mock

import pytest
from core.api import RouteRequest
from core.metrics import MetricName, MetricsClient, MetricType


@mock.patch("core.logger.logger.uuid4", return_value="uuid")
class TestMetricsClient:
    @pytest.mark.parametrize(
        "api_key, expected_user_type",
        [
            ("local-admin-api-key", MetricType.ADMIN.value),
            (None, MetricType.USER.value),
        ],
    )
    def test_log_metric(
        self,
        mock_uuid4: mock.Mock,
        api_key: str | None,
        expected_user_type: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        route_request = RouteRequest(
            headers={"x-api-key": api_key} if api_key else {},
        )
        monkeypatch.setenv("ADMIN_API_KEY", "local-admin-api-key")
        client = MetricsClient(route_request)

        with mock.patch("builtins.print") as mock_print:
            client.log_metric(MetricName.TEST)

        assert mock_print.call_count == 1
        assert mock_print.call_args[0][0] == f"[uuid][metrics][{expected_user_type}] test"
