from typing import Callable

import pytest
from django.test import Client
from django.urls import reverse

from feature.flags import ENABLE_SENTRY_TESTING_ENDPOINT


@pytest.mark.django_db
class TestSentry:
    def test_redirect_returned_when_flag_is_disabled(self) -> None:
        client = Client()

        response = client.get("/feature/test-sentry")

        assert response.status_code == 302
        assert response["Location"] == reverse("home")

    def test_error_raised_when_flag_is_enabled(self, enable_flag: Callable[[str], None]) -> None:
        enable_flag(ENABLE_SENTRY_TESTING_ENDPOINT)
        client = Client()

        with pytest.raises(ZeroDivisionError):
            client.get("/feature/test-sentry")
