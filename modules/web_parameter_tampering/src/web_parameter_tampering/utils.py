import os


def get_headers() -> dict[str, str]:
    return {
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": os.environ.get("ALLOW_ORIGIN") or "",
    }
