from django.test import RequestFactory

from web_parameter_tampering.views import wpt


class Test:
    def test(self) -> None:
        request = RequestFactory().get("/")

        response = wpt(request)

        assert response.status_code == 200
        assert b"Web Parameter Tampering Demo - WIP" == response.content
