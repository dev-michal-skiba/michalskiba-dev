import os

from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

IS_SENTRY_ENABLED = os.getenv("ENVIRONMENT", "").lower() == "production"
SENTRY_INIT_OPTIONS = {
    "dsn": os.getenv("SENTRY_DSN"),
    "send_default_pii": True,
    "integrations": [
        AwsLambdaIntegration(),
    ],
}
