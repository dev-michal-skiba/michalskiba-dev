from typing import Type
from unittest.mock import Mock, patch

import pytest
from core.logger import Logger, LogGroupLogger, PrintLogger, get_logger
from freezegun import freeze_time


@patch("core.logger.logger.uuid4", return_value="uuid")
class TestPrintLogger:
    def test_log(self, mock_uuid4: Mock) -> None:
        logger = PrintLogger(keys=["a", "b", "c"])

        with patch("builtins.print") as mock_print:
            logger.log("test")

        mock_print.assert_called_once_with("[uuid][a][b][c] test")


@patch("core.logger.logger.uuid4", return_value="uuid")
@patch("core.logger.logger.boto3.client")
@freeze_time("2025-06-03 21:00:00")
class TestLogGroupLogger:
    def test_log(
        self, mock_boto3: Mock, mock_uuid4: Mock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("LOG_GROUP_NAME", "test-log-group-name")
        logger = LogGroupLogger(keys=["a", "b", "c"])
        mock_boto3.assert_called_once_with("logs")
        mock_boto3.return_value.create_log_stream.assert_called_once_with(
            logGroupName="test-log-group-name",
            logStreamName="default",
        )

        logger.log("test")

        mock_boto3.return_value.put_log_events.assert_called_once_with(
            logGroupName="test-log-group-name",
            logStreamName="default",
            logEvents=[
                {
                    "timestamp": 1748984400000,
                    "message": "[uuid][a][b][c] test",
                }
            ],
        )


@patch("core.logger.logger.boto3.client")
class TestGetLogger:
    @pytest.mark.parametrize(
        "environment, expected_logger_class",
        [
            ("Local", PrintLogger),
            ("AnyOtherEnvironment", PrintLogger),
            ("Production", LogGroupLogger),
        ],
        ids=["local", "any_other_environment", "production"],
    )
    def test_get_logger(
        self,
        mock_boto3: Mock,
        environment: str,
        expected_logger_class: Type[Logger],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("ENVIRONMENT", environment)

        logger = get_logger(keys=["a", "b", "c"])

        assert isinstance(logger, expected_logger_class)
