import json
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
import pytest
from freezegun import freeze_time
from host_header_injection.exception import HTTPException
from host_header_injection.utils import (
    extract_token_and_new_password,
    generate_reset_link,
    get_email,
    get_headers,
    get_host,
    get_secure_version_flag,
    update_password,
    validate_token,
)


class TestGetHeaders:
    def test_correct_headers(self) -> None:
        headers = get_headers()

        assert headers == {
            "Access-Control-Allow-Origin": "http://localhost:8080",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Credentials": "true",
        }


class TestGetEmail:
    def test_valid_email(self) -> None:
        event = {"body": json.dumps({"email": "test@example.com"})}
        email = get_email(event)
        assert email == "test@example.com"

    def test_invalid_json_body(self) -> None:
        with pytest.raises(HTTPException) as exc_info:
            get_email({"body": "not a json body"})
        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Invalid JSON body"

    def test_missing_email_in_body(self) -> None:
        event = {"body": json.dumps({"other_field": "value"})}
        with pytest.raises(HTTPException) as exc_info:
            get_email(event)
        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Invalid email"

    def test_invalid_email_format(self) -> None:
        event = {"body": json.dumps({"email": "invalid-email"})}
        with pytest.raises(HTTPException) as exc_info:
            get_email(event)
        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Invalid email"


class TestGetSecureVersionFlag:
    def test_empty_query_string_parameters(self) -> None:
        event: dict[str, Any] = {"queryStringParameters": {}}
        assert get_secure_version_flag(event) is True

    @pytest.mark.parametrize(
        "flag_value", ["false", "FALSE", "FaLsE"], ids=["lowercase", "uppercase", "mixed_case"]
    )
    def test_parameter_false(self, flag_value: str) -> None:
        event = {"queryStringParameters": {"is_secure_version_on": flag_value}}
        assert get_secure_version_flag(event) is False

    @pytest.mark.parametrize(
        "flag_value", ["true", "TRUE", "TrUe"], ids=["lowercase", "uppercase", "mixed_case"]
    )
    def test_parameter_true(self, flag_value: str) -> None:
        event = {"queryStringParameters": {"is_secure_version_on": flag_value}}
        assert get_secure_version_flag(event) is True


class TestGetHost:
    def test_secure_version_on(self) -> None:
        event: dict[str, Any] = {}
        assert get_host(event, is_secure_version_on=True) == "http://localhost:8080"

    def test_missing_allow_origin(self, monkeypatch: pytest.MonkeyPatch) -> None:
        event = {"headers": {"Host": "test-host.com"}}
        monkeypatch.delenv("ALLOW_ORIGIN", raising=False)
        with pytest.raises(HTTPException) as exc_info:
            get_host(event, is_secure_version_on=True)
        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Internal server error"

    @pytest.mark.parametrize(
        "headers,expected_host",
        [
            ({"Host": "test-host.com"}, "https://test-host.com"),
            ({"X-Forwarded-Host": "forwarded-host.com"}, "https://forwarded-host.com"),
            (
                {"Host": "test-host.com", "X-Forwarded-Host": "forwarded-host.com"},
                "https://forwarded-host.com",
            ),
            ({"Host": "a.test-host.com"}, "https://test-host.com"),
            ({"Host": "b.a.test-host.com"}, "https://test-host.com"),
            ({"Host": "c.b.a.test-host.com"}, "https://test-host.com"),
        ],
        ids=[
            "host_header",
            "x_forwarded_host",
            "both_headers",
            "single_subdomain",
            "double_subdomain",
            "triple_subdomain",
        ],
    )
    def test_host_headers(
        self, headers: dict[str, str], expected_host: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        event = {"headers": headers}
        monkeypatch.setenv("ALLOW_ORIGIN", expected_host)
        assert get_host(event, is_secure_version_on=False) == expected_host

    def test_missing_headers(self) -> None:
        event: dict[str, Any] = {"headers": {}}
        with pytest.raises(HTTPException) as exc_info:
            get_host(event, is_secure_version_on=False)
        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Invalid host header"


class TestGenerateResetLink:
    @freeze_time("2025-01-15 14:00:00")
    def test_link_generated_correctly(self, monkeypatch: pytest.MonkeyPatch) -> None:
        email = "test@example.com"
        host = "https://test-host.com"
        secret_key = "test-secret-key"

        reset_link = generate_reset_link(email, host)

        token = reset_link.split("token=")[1]
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        assert decoded["email"] == email

        expiry = datetime.fromtimestamp(decoded["exp"], timezone.utc)
        assert expiry == datetime(2025, 1, 15, 14, 15, 0, tzinfo=timezone.utc)
        assert (
            reset_link
            == f"{host}/demos/host-header-injection/password-reset/complete?token={token}"
        )

    def test_missing_secret_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("SECRET_KEY", raising=False)

        with pytest.raises(HTTPException) as exc_info:
            generate_reset_link("test@example.com", "https://test-host.com")

        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Internal server error"


class TestExtractTokenAndNewPassword:
    def test_valid_token_and_new_password(self) -> None:
        event = {"body": json.dumps({"token": "test-token", "password": "new-password"})}

        token, new_password = extract_token_and_new_password(event)

        assert token == "test-token"
        assert new_password == "new-password"

    @pytest.mark.parametrize(
        "body",
        [
            {"body": json.dumps({"password": "new-password"})},
            {"body": json.dumps({"token": "test-token"})},
            {"body": json.dumps({})},
        ],
        ids=["missing_token", "missing_password", "missing_both"],
    )
    def test_missing_token(self, body: dict[str, Any]) -> None:
        with pytest.raises(HTTPException) as exc_info:
            extract_token_and_new_password(body)

        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Please provide token and new password"


class TestValidateToken:
    def test_valid_token(self) -> None:
        secret_key = "test-secret-key"
        expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
        token = jwt.encode(
            {"email": "test@example.com", "exp": expiry.timestamp()},
            secret_key,
            algorithm="HS256",
        )

        assert validate_token(token) is None

    def test_expired_token(self) -> None:
        secret_key = "test-secret-key"
        expiry = datetime.now(timezone.utc) - timedelta(minutes=1)
        token = jwt.encode(
            {"email": "test@example.com", "exp": expiry.timestamp()},
            secret_key,
            algorithm="HS256",
        )

        with pytest.raises(HTTPException) as exc_info:
            validate_token(token)

        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Token has expired"

    def test_invalid_token(self) -> None:
        token = "invalid-token"

        with pytest.raises(HTTPException) as exc_info:
            validate_token(token)

        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Invalid token"

    def test_missing_secret_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("SECRET_KEY", raising=False)

        with pytest.raises(HTTPException) as exc_info:
            validate_token("test-token")

        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Internal server error"


class TestUpdatePassword:
    def test_update_password(self) -> None:
        assert update_password(token="test-token", new_password="new-password") is None
