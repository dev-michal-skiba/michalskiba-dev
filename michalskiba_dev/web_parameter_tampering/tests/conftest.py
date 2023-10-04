import jwt
import pytest
from django.conf import settings

from demo.models import DemoUser
from web_parameter_tampering.models import PressApplication


@pytest.fixture
def hacker_press_application() -> PressApplication:
    return PressApplication.objects.get(user__username="hacker")


@pytest.fixture
def hacker_auth_token(hacker: DemoUser) -> str:
    auth_token_payload = {"username": "hacker", "expiry": "9999-06-28 12:30:00 +0000"}
    encoded_user_info = jwt.encode(auth_token_payload, settings.SECRET_KEY, algorithm="HS256")
    return encoded_user_info
