from django.test import Client


class TestHome:
    def test_renders_home_template(self) -> None:
        client = Client()

        response = client.get("/")

        assert response.status_code == 200
        assert "home.html" in (t.name for t in response.templates)


class TestAboutMe:
    def test_renders_about_me_template(self) -> None:
        client = Client()

        response = client.get("/about-me")

        assert response.status_code == 200
        assert "about_me.html" in (t.name for t in response.templates)
