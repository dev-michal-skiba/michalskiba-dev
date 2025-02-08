from host_header_injection.utils import get_headers


class TestGetHeaders:
    def test_correct_headers(self) -> None:
        headers = get_headers()

        assert headers == {
            "Access-Control-Allow-Origin": "http://localhost:1313",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Credentials": "true",
        }
