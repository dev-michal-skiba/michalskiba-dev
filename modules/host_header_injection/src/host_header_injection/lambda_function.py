from core.api import (
    LambdaContext,
    LambdaEvent,
    LambdaResponse,
    Route,
    Router,
    RouteRequest,
    RouteResponse,
)
from core.sentry import IS_SENTRY_ENABLED, SENTRY_INIT_OPTIONS, sentry_init

from .utils import (
    extract_token_and_new_password,
    generate_reset_link,
    get_email,
    get_host,
    get_secure_version_flag,
    update_password,
    validate_token,
)

if IS_SENTRY_ENABLED:
    sentry_init(**SENTRY_INIT_OPTIONS)


def initiate_password_reset(request: RouteRequest) -> RouteResponse:
    email = get_email(request)
    is_secure_version_on = get_secure_version_flag(request)
    host = get_host(request, is_secure_version_on)
    reset_link = generate_reset_link(email, host)
    return RouteResponse(status_code=200, body={"reset_link": reset_link})


def complete_password_reset(request: RouteRequest) -> RouteResponse:
    token, new_password = extract_token_and_new_password(request)
    validate_token(token)
    update_password(token, new_password)
    return RouteResponse(status_code=204)


router = Router()
router.add_route(
    Route(
        path="/api/demo/host-header-injection/password-reset/initiate",
        method="POST",
        handler=initiate_password_reset,
    )
)
router.add_route(
    Route(
        path="/api/demo/host-header-injection/password-reset/complete",
        method="POST",
        handler=complete_password_reset,
    )
)


def lambda_handler(event: LambdaEvent, context: LambdaContext) -> LambdaResponse:
    return router(event)
