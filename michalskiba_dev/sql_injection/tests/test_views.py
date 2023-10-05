from django.test import RequestFactory

from sql_injection.views import home


class TestHome:
    def test_view_returns_successful_response(self) -> None:
        request = RequestFactory().get("/")

        response = home(request)

        assert response.status_code == 200
        assert response.content == b"SQL Injection WIP"
