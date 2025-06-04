from core.api import (
    AuthorizerResponse,
    AuthorizerRoute,
    LambdaContext,
    LambdaEvent,
    LambdaResponse,
    Route,
    Router,
    RouteRequest,
    RouteResponse,
)
from core.sentry import IS_SENTRY_ENABLED, SENTRY_INIT_OPTIONS, sentry_init

from .domain import User
from .utils import get_headers

if IS_SENTRY_ENABLED:
    sentry_init(**SENTRY_INIT_OPTIONS)


def authorize(request: RouteRequest) -> AuthorizerResponse:
    access_token = request.cookies.get("access_token")
    if access_token is None:
        return AuthorizerResponse(is_authorized=False)
    user = User.from_access_token(access_token)
    if user is None:
        return AuthorizerResponse(is_authorized=False)
    return AuthorizerResponse(is_authorized=True, username=user.username)


def login(request: RouteRequest) -> RouteResponse:
    username = request.body.get("username") or ""
    password = request.body.get("password") or ""
    user = User.from_credentials(username, password)
    if user is None:
        return RouteResponse(status_code=401)
    return RouteResponse(status_code=200, headers=get_headers(access_token=user.access_token))


def logout(request: RouteRequest) -> RouteResponse:
    return RouteResponse(status_code=200, headers=get_headers(access_token=""))


router = Router()
router.add_route(AuthorizerRoute(handler=authorize))
router.add_route(Route(path="/api/demo/auth/login", method="POST", handler=login))
router.add_route(Route(path="/api/demo/auth/logout", method="POST", handler=logout))


def lambda_handler(event: LambdaEvent, context: LambdaContext) -> LambdaResponse:
    return router(event)
