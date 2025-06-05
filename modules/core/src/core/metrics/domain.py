from enum import Enum


class MetricName(Enum):
    WPT_EXPLOIT = "wpt-exploit"


class MetricType(Enum):
    ADMIN = "admin"
    USER = "user"
