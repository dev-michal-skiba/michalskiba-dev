from freezegun import freeze_time
from host_header_injection.lambda_function import lambda_handler


class TestLambdaHandler:
    @freeze_time("2025-01-15 14:00:00")
    def test_secure_version(self) -> None:
        event = {
            "rawPath": "/demo/host-header-injection/password-reset/initiate",
            "body": '{"email": "test@example.com"}',
            "queryStringParameters": {"is_secure_version_on": "true"},
            "headers": {"Host": "test-host.com", "X-Forwarded-Host": "evil-host.com"},
        }

        response = lambda_handler(event=event, context={})

        assert response == {
            "statusCode": 200,
            "body": '{"reset_link": "http://localhost:1313/demo/host-header-injection/password-reset/complete?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzY5NTA1MDAuMH0.u_Jq2ySry2eme_RQkktBJTsUZ0lBbcqNh4xA_-1Xcro"}',
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            },
        }

    @freeze_time("2025-01-15 14:00:00")
    def test_insecure_version_with_malicious_header(self) -> None:
        event = {
            "rawPath": "/demo/host-header-injection/password-reset/initiate",
            "body": '{"email": "test@example.com"}',
            "queryStringParameters": {"is_secure_version_on": "false"},
            "headers": {"Host": "test-host.com", "X-Forwarded-Host": "evil-host.com"},
        }

        response = lambda_handler(event=event, context={})

        assert response == {
            "statusCode": 200,
            "body": '{"reset_link": "https://evil-host.com/demo/host-header-injection/password-reset/complete?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzY5NTA1MDAuMH0.u_Jq2ySry2eme_RQkktBJTsUZ0lBbcqNh4xA_-1Xcro"}',
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:1313",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            },
        }
