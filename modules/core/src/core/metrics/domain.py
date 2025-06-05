from enum import Enum


class MetricName(Enum):
    WPT_EXPLOIT = "wpt-exploit"
    SQLI_EXPLOIT = "sqli-exploit"
    HHI_EXPLOIT = "hhi-exploit"


class MetricType(Enum):
    ADMIN = "admin"
    USER = "user"
