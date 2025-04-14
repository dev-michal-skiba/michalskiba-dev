from auth.utils import get_headers


class TestGetHeaders:
    def test_correct_headers(self) -> None:
        headers = get_headers(access_token="token")

        assert headers == {
            "Set-Cookie": "access_token=token; Secure; HttpOnly; SameSite=Lax; Path=/api/demo",
        }
