import datetime
import os
from abc import ABC, abstractmethod
from uuid import uuid4

import boto3


class Logger(ABC):
    def __init__(self, keys: list[str]):
        self._key = "".join(f"[{k}]" for k in [str(uuid4())] + keys)

    @abstractmethod
    def log(self, message: str) -> None:
        pass


class PrintLogger(Logger):
    def __init__(self, keys: list[str]):
        super().__init__(keys)

    def log(self, message: str) -> None:
        print(f"{self._key} {message}")


class LogGroupLogger(Logger):
    def __init__(self, keys: list[str]):
        super().__init__(keys)
        self._client = boto3.client("logs")
        self._log_group_name = os.getenv("LOG_GROUP_NAME")
        self._log_stream_name = "default"
        self._ensure_stream_exists()

    def _ensure_stream_exists(self) -> None:
        try:
            self._client.create_log_stream(
                logGroupName=self._log_group_name, logStreamName=self._log_stream_name
            )
        except self._client.exceptions.ResourceAlreadyExistsException:
            pass

    def log(self, message: str) -> None:
        self._client.put_log_events(
            logGroupName=self._log_group_name,
            logStreamName=self._log_stream_name,
            logEvents=[
                {
                    "timestamp": int(datetime.datetime.now().timestamp() * 1000),
                    "message": f"{self._key} {message}",
                }
            ],
        )


def get_logger(keys: list[str]) -> Logger:
    environment = os.getenv("ENVIRONMENT")
    if environment and environment.lower() == "production":
        return LogGroupLogger(keys)
    return PrintLogger(keys)
