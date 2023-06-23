from django.test import RequestFactory

from web_parameter_tampering.views import home


class TestHome:
    def test_request_succeeds(self) -> None:
        request = RequestFactory().get("/")

        response = home(request)

        assert response.status_code == 200
