from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
import pytest
from core.api import HttpException, RouteRequest
from freezegun import freeze_time
from host_header_injection.utils import (
    extract_token_and_new_password,
    generate_reset_link,
    get_email,
    get_host,
    get_secure_version_flag,
    update_password,
    validate_token,
)


class TestGetEmail:
    def test_valid_email(self) -> None:
        request = RouteRequest(body={"email": "test@example.com"})

        email = get_email(request)

        assert email == "test@example.com"

    def test_missing_email_in_body(self) -> None:
        request = RouteRequest(body={"other_field": "value"})

        with pytest.raises(HttpException) as exc_info:
            get_email(request)

        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Invalid email"

    def test_invalid_email_format(self) -> None:
        request = RouteRequest(body={"email": "invalid-email"})

        with pytest.raises(HttpException) as exc_info:
            get_email(request)

        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Invalid email"


class TestGetSecureVersionFlag:
    def test_empty_query_string_parameters(self) -> None:
        request = RouteRequest()
        assert get_secure_version_flag(request) is True

    @pytest.mark.parametrize(
        "flag_value", ["false", "FALSE", "FaLsE"], ids=["lowercase", "uppercase", "mixed_case"]
    )
    def test_parameter_false(self, flag_value: str) -> None:
        request = RouteRequest(query_paramaters={"is_secure_version_on": flag_value})
        assert get_secure_version_flag(request) is False

    @pytest.mark.parametrize(
        "flag_value", ["true", "TRUE", "TrUe"], ids=["lowercase", "uppercase", "mixed_case"]
    )
    def test_parameter_true(self, flag_value: str) -> None:
        request = RouteRequest(query_paramaters={"is_secure_version_on": flag_value})
        assert get_secure_version_flag(request) is True


class TestGetHost:
    def test_secure_version_on(self) -> None:
        request = RouteRequest()
        assert get_host(request, is_secure_version_on=True) == "https://localhost:8080"

    def test_missing_domain(self, monkeypatch: pytest.MonkeyPatch) -> None:
        request = RouteRequest(headers={"origin": "https://test-host.com"})
        monkeypatch.delenv("DOMAIN", raising=False)
        with pytest.raises(HttpException) as exc_info:
            get_host(request, is_secure_version_on=True)
        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Internal server error"

    @pytest.mark.parametrize(
        "headers,expected_host",
        [
            ({"origin": "https://test-host.com"}, "https://test-host.com"),
            ({"x-forwarded-host": "forwarded-host.com"}, "https://forwarded-host.com"),
            (
                {"origin": "https://test-host.com", "x-forwarded-host": "forwarded-host.com"},
                "https://forwarded-host.com",
            ),
            ({"origin": "https://a.test-host.com"}, "https://a.test-host.com"),
            ({"origin": "https://b.a.test-host.com"}, "https://b.a.test-host.com"),
            ({"origin": "https://c.b.a.test-host.com"}, "https://c.b.a.test-host.com"),
        ],
        ids=[
            "origin_header",
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
        request = RouteRequest(headers=headers)
        monkeypatch.setenv("DOMAIN", expected_host)
        assert get_host(request, is_secure_version_on=False) == expected_host

    def test_missing_headers(self) -> None:
        request = RouteRequest()
        with pytest.raises(HttpException) as exc_info:
            get_host(request, is_secure_version_on=False)
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
            == f"{host}/demo/host-header-injection/password-reset/complete/?token={token}"
        )

    def test_missing_secret_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("SECRET_KEY", raising=False)

        with pytest.raises(HttpException) as exc_info:
            generate_reset_link("test@example.com", "https://test-host.com")

        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Internal server error"


class TestExtractTokenAndNewPassword:
    def test_valid_token_and_new_password(self) -> None:
        request = RouteRequest(body={"token": "test-token", "password": "new-password"})

        token, new_password = extract_token_and_new_password(request)

        assert token == "test-token"
        assert new_password == "new-password"

    @pytest.mark.parametrize(
        "body",
        [
            {"password": "new-password"},
            {"token": "test-token"},
            {},
        ],
        ids=["missing_token", "missing_password", "missing_both"],
    )
    def test_missing_token(self, body: dict[str, Any]) -> None:
        request = RouteRequest(body=body)

        with pytest.raises(HttpException) as exc_info:
            extract_token_and_new_password(request)

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

        with pytest.raises(HttpException) as exc_info:
            validate_token(token)

        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Token has expired"

    def test_invalid_token(self) -> None:
        token = "invalid-token"

        with pytest.raises(HttpException) as exc_info:
            validate_token(token)

        assert exc_info.value.status_code == 400
        assert str(exc_info.value.detail) == "Invalid token"

    def test_missing_secret_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("SECRET_KEY", raising=False)

        with pytest.raises(HttpException) as exc_info:
            validate_token("test-token")

        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Internal server error"


class TestUpdatePassword:
    def test_update_password(self) -> None:
        assert update_password(token="test-token", new_password="new-password") is None
