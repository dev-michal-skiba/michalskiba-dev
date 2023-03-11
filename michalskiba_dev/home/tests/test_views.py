from django.test import Client


class TestHome(object):
    def test_renders_home_template(self):
        client = Client()

        response = client.get("/")

        assert response.status_code == 200
        assert "home.html" in (t.name for t in response.templates)
