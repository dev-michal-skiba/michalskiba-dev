from unittest.mock import Mock, patch

import pytest
from django.http import Http404
from django.shortcuts import redirect
from django.test import RequestFactory

from web_parameter_tampering.constants import (
    AUTH_TOKEN_COOKIE_NAME,
    IS_SECURE_VERSION_ON_COOKIE_NAME,
)
from web_parameter_tampering.models import User
from web_parameter_tampering.views import (
    home,
    login,
    logout,
    press,
    press_insecure,
    tickets,
)


@pytest.mark.django_db(databases=["web_parameter_tampering"])
class TestHome:
    def test_request_succeeds_for_not_authenticated_user(self) -> None:
        request = RequestFactory().get("/")

        response = home(request, *[], **{})

        assert b"Logout" not in response.content
        assert b"<h1>Live your best life on BEST Festival</h1>" in response.content
        assert response.status_code == 200

    def test_request_succeeds_for_authenticated_user(self, hacker_auth_token: str) -> None:
        request = RequestFactory().get("/")
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        response = home(request, *[], **{})

        assert b"Logout" in response.content
        assert b"<h1>Live your best life on BEST Festival</h1>" in response.content
        assert response.status_code == 200


@pytest.mark.django_db(databases=["web_parameter_tampering"])
class TestTickets:
    def test_request_succeeds_for_not_authenticated_user(self) -> None:
        request = RequestFactory().get("/tickets")

        response = tickets(request, *[], **{})

        assert b"Logout" not in response.content
        assert b"<h1>Tickets coming for sale soon</h1>" in response.content
        assert response.status_code == 200

    def test_request_succeeds_for_authenticated_user(self, hacker_auth_token: str) -> None:
        request = RequestFactory().get("/tickets")
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        response = tickets(request, *[], **{})

        assert b"Logout" in response.content
        assert b"<h1>Tickets coming for sale soon</h1>" in response.content
        assert response.status_code == 200


@pytest.mark.django_db(databases=["web_parameter_tampering"])
class TestLogin:
    def test_user_not_set_for_get(self) -> None:
        request = RequestFactory().get("/login")

        response = login(request)

        assert response.status_code == 302
        assert response["Location"] == "/press"
        assert AUTH_TOKEN_COOKIE_NAME not in str(response.cookies)

    def test_user_not_set_for_post_and_wrong_credentials(self) -> None:
        request = RequestFactory().post(
            "/login", data={"username": "hacker", "password": "Hacker1234?"}
        )

        response = login(request)

        assert response.status_code == 302
        assert response["Location"] == "/press"
        assert AUTH_TOKEN_COOKIE_NAME not in str(response.cookies)

    def test_user_set_for_post_and_correct_credentials(self) -> None:
        request = RequestFactory().post(
            "/login", data={"username": "hacker", "password": "Hacker1234!"}
        )

        response = login(request)

        assert response.status_code == 302
        assert response["Location"] == "/press"
        assert AUTH_TOKEN_COOKIE_NAME in str(response.cookies)


@pytest.mark.django_db(databases=["web_parameter_tampering"])
@patch("web_parameter_tampering.views.clear_user")
class TestLogout:
    def test_auth_token_is_not_cleaned_on_get(
        self, clear_user_mock: Mock, hacker_auth_token: str
    ) -> None:
        request = RequestFactory().get("/logout")
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        response = logout(request, *[], **{})

        assert response.status_code == 302
        assert response["Location"] == "/press"
        assert clear_user_mock.call_count == 0

    def test_auth_token_is_not_cleaned_on_post_when_auth_token_is_missing(
        self, clear_user_mock: Mock
    ) -> None:
        request = RequestFactory().post("/logout")

        response = logout(request, *[], **{})

        assert response.status_code == 302
        assert response["Location"] == "/press"
        assert clear_user_mock.call_count == 0

    def test_auth_token_is_cleaned_on_post(
        self, clear_user_mock: Mock, hacker_auth_token: str
    ) -> None:
        clear_user_mock.return_value = redirect("/press")
        request = RequestFactory().post("/logout")
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        response = logout(request, *[], **{})

        assert response.status_code == 302
        assert response["Location"] == "/press"
        assert clear_user_mock.call_count == 1


@pytest.mark.django_db(databases=["web_parameter_tampering"])
class TestPress:
    @pytest.mark.parametrize("is_secure_version_on", ("False", "True"))
    def test_renders_login_page_for_not_authenticated_user(
        self, is_secure_version_on: str
    ) -> None:
        request = RequestFactory().get("/press")
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = is_secure_version_on

        response = press(request, *[], **{})

        assert response.status_code == 200
        assert b"Logout" not in response.content
        assert (
            b"To see status of your press application please log in to our "
            b"BEST Festival press portal" in response.content
        )

    def test_redirects_to_insecure_press_view_when_user_is_authenticated_and_secure_off(
        self, hacker_auth_token: str, hacker: User
    ) -> None:
        request = RequestFactory().get("/press")
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = "false"
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        response = press(request, *[], **{})

        assert response.status_code == 302
        assert response["Location"] == f"/press/{hacker.pk}"

    def test_renders_press_application_when_user_is_authenticated_and_secure_on(
        self, hacker_auth_token: str, hacker: User
    ) -> None:
        request = RequestFactory().get("/press")
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = "true"
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        response = press(request, *[], **{})

        assert response.status_code == 200
        assert b"Logout" in response.content
        assert b"<h1>Accreditation info</h1>" in response.content


@pytest.mark.django_db(databases=["web_parameter_tampering"])
class TestPressInsecure:
    @pytest.mark.parametrize(
        "is_user_authenticated, is_secure_version_on",
        ((False, "False"), (False, "True"), (True, "True")),
    )
    def test_redirects_to_press_when_user_is_unauthenticated_or_secure_version_on(
        self,
        hacker_auth_token: str,
        hacker: User,
        is_user_authenticated: bool,
        is_secure_version_on: str,
    ) -> None:
        request = RequestFactory().get(f"/press/{hacker.pk}")
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = is_secure_version_on
        if is_user_authenticated:
            request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        response = press_insecure(request, *[], **{"user_pk": hacker.pk})

        assert response.status_code == 302
        assert response["Location"] == "/press"

    def test_returns_404_on_non_existing_user_pk(
        self, hacker_auth_token: str, hacker: User, victim: User
    ) -> None:
        user_pk = max(hacker.pk, victim.pk) + 1
        request = RequestFactory().get(f"/press/{user_pk}")
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = "false"
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        with pytest.raises(Http404) as exc:
            press_insecure(request, *[], **{"user_pk": user_pk})

        assert exc.value.args[0] == "No User matches the given query."

    def test_returns_press_application_for_query_user_not_for_authenticated_user(
        self, hacker_auth_token: str, hacker: User, victim: User
    ) -> None:
        request = RequestFactory().get(f"/press/{victim.pk}")
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = "false"
        request.COOKIES[AUTH_TOKEN_COOKIE_NAME] = hacker_auth_token

        response = press_insecure(request, *[], **{"user_pk": victim.pk})

        assert response.status_code == 200
        assert b"Logout" in response.content
        assert b"<h1>Accreditation info</h1>" in response.content
        assert b"<p>Organization: Legitimate organization</p>" in response.content
