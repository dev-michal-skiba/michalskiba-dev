from core.api import (
    HttpException,
    LambdaContext,
    LambdaEvent,
    LambdaResponse,
    Route,
    Router,
    RouteRequest,
    RouteResponse,
)

from .db import get_press_application
from .utils import get_username


def get_press_application_route_handler(request: RouteRequest) -> RouteResponse:
    username = get_username(request)
    if username is None:
        raise HttpException(status_code=404, detail="User not found")
    press_application = get_press_application(username)
    if press_application is None:
        raise HttpException(status_code=404, detail="Press application not found")
    return RouteResponse(
        status_code=200,
        body={
            "accreditation_code": press_application.accreditation_code,
            "organization": press_application.organization,
        },
    )


router = Router()
router.add_route(
    Route(
        path="/api/demo/web-parameter-tampering/press-application",
        method="GET",
        handler=get_press_application_route_handler,
    )
)


def lambda_handler(event: LambdaEvent, context: LambdaContext) -> LambdaResponse:
    return router(event)
