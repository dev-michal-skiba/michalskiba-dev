import os


def get_headers(access_token: str) -> dict[str, str]:
    headers = {}
    cookie_template = os.environ.get("COOKIE_TEMPLATE")
    if cookie_template is not None:
        headers["Set-Cookie"] = cookie_template.format(access_token)
    return headers
