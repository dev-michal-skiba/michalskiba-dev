import logging
from datetime import datetime, timedelta

import jwt
import pytz
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from jwt import PyJWTError

from web_parameter_tampering.constants import (
    AUTH_TOKEN_COOKIE_NAME,
    IS_SECURE_VERSION_ON_COOKIE_NAME,
    TIME_FORMAT,
)
from web_parameter_tampering.models import User

logger = logging.getLogger(__name__)


def get_is_secure_version_on(request: HttpRequest) -> bool:
    value = request.COOKIES.get(IS_SECURE_VERSION_ON_COOKIE_NAME, "true")
    return value.lower() == "true"


def set_is_secure_version_on(response: HttpResponse, value: bool) -> HttpResponse:
    raw_value = "true" if value else "false"
    response.set_cookie(
        key=IS_SECURE_VERSION_ON_COOKIE_NAME,
        value=raw_value,
        secure=True,
        samesite="Lax",
    )
    return response


def get_user(request: HttpRequest) -> User | None:
    auth_token = request.COOKIES.get(AUTH_TOKEN_COOKIE_NAME)
    if not auth_token:
        return None
    try:
        user_info = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=["HS256"])
        username = str(user_info["username"])
        expiry = datetime.strptime(user_info["expiry"], TIME_FORMAT)
        now = datetime.now(tz=pytz.utc)
        if now >= expiry:
            return None
        user = User.objects.get(username=username)
    except PyJWTError:
        return None
    except KeyError:
        logger.warning("Missing required keys in '%s' auth token", auth_token)
        return None
    except ValueError:
        logger.warning("Failed to get expiry datetime from '%s' auth token", auth_token)
        return None
    except User.DoesNotExist:
        logger.warning("Failed to get user from '%s' auth token", auth_token)
        return None
    return user


def set_user(response: HttpResponseRedirect, user: User) -> HttpResponseRedirect:
    expiry = datetime.now(tz=pytz.utc) + timedelta(days=7)
    auth_token_payload = {
        "username": user.username,
        "expiry": expiry.strftime(TIME_FORMAT),
    }
    encoded_user_info = jwt.encode(auth_token_payload, settings.SECRET_KEY, algorithm="HS256")
    response.set_cookie(
        key=AUTH_TOKEN_COOKIE_NAME,
        value=encoded_user_info,
        secure=True,
        samesite="Lax",
        httponly=True,
    )
    return response


def clear_user(response: HttpResponseRedirect) -> HttpResponseRedirect:
    response.delete_cookie(key=AUTH_TOKEN_COOKIE_NAME)
    return response
