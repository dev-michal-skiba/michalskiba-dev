from django.test import RequestFactory

from web_parameter_tampering.views import home, press, tickets


class TestHome:
    def test_request_succeeds(self) -> None:
        request = RequestFactory().get("/")

        response = home(request)

        assert response.status_code == 200


class TestTickets:
    def test_request_succeeds(self) -> None:
        request = RequestFactory().get("/tickets")

        response = tickets(request)

        assert response.status_code == 200


class TestPress:
    def test_request_succeeds(self) -> None:
        request = RequestFactory().get("/press")

        response = press(request, *[], **{})

        assert response.status_code == 200
