from datetime import datetime, timedelta, timezone

import jwt
from freezegun import freeze_time
from host_header_injection.lambda_function import lambda_handler


class TestPasswordResetInitiate:
    @freeze_time("2025-01-15 14:00:00")
    def test_secure_version(self) -> None:
        event = {
            "body": '{"email": "test@example.com"}',
            "queryStringParameters": {"is_secure_version_on": "true"},
            "headers": {"Host": "test-host.com", "X-Forwarded-Host": "evil-host.com"},
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/api/demo/host-header-injection/password-reset/initiate",
                }
            },
        }

        response = lambda_handler(event=event, context={})

        assert response == {
            "statusCode": 200,
            "body": '{"reset_link": "http://localhost:8080/demos/host-header-injection/password-reset/complete/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzY5NTA1MDAuMH0.u_Jq2ySry2eme_RQkktBJTsUZ0lBbcqNh4xA_-1Xcro"}',
        }

    @freeze_time("2025-01-15 14:00:00")
    def test_insecure_version_with_malicious_header(self) -> None:
        event = {
            "body": '{"email": "test@example.com"}',
            "queryStringParameters": {"is_secure_version_on": "false"},
            "headers": {"Host": "test-host.com", "X-Forwarded-Host": "evil-host.com"},
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/api/demo/host-header-injection/password-reset/initiate",
                }
            },
        }

        response = lambda_handler(event=event, context={})

        assert response == {
            "statusCode": 200,
            "body": '{"reset_link": "https://evil-host.com/demos/host-header-injection/password-reset/complete/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzY5NTA1MDAuMH0.u_Jq2ySry2eme_RQkktBJTsUZ0lBbcqNh4xA_-1Xcro"}',
        }


class TestCompletePasswordReset:
    def test_complete_password_reset(self) -> None:
        secret_key = "test-secret-key"
        expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
        token = jwt.encode(
            {"email": "test@example.com", "exp": expiry.timestamp()},
            secret_key,
            algorithm="HS256",
        )
        event = {
            "body": f'{{"token": "{token}", "password": "new-password"}}',
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/api/demo/host-header-injection/password-reset/complete",
                }
            },
        }

        response = lambda_handler(event=event, context={})

        assert response == {"statusCode": 204}
