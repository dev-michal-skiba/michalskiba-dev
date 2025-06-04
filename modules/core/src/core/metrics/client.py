import os

from ..api import RouteRequest
from ..logger import get_logger
from .domain import MetricName, MetricType


class MetricsClient:
    def __init__(self, route_request: RouteRequest):
        self._logger = get_logger(
            [
                "metrics",
                self._get_user_type(route_request).value,
            ]
        )

    def _get_user_type(self, route_request: RouteRequest) -> MetricType:
        api_key = route_request.headers.get("x-api-key")
        admin_api_key = os.getenv("ADMIN_API_KEY")
        if admin_api_key and admin_api_key == api_key:
            return MetricType.ADMIN
        return MetricType.USER

    def log_metric(self, metric_name: MetricName) -> None:
        self._logger.log(metric_name.value)
