import json

from core.api import (
    LambdaContext,
    LambdaEvent,
    LambdaResponse,
    Route,
    Router,
    RouteRequest,
    RouteResponse,
)

from . import db, utils


def get_parcel_stores(request: RouteRequest) -> RouteResponse:
    address_search_phrase, is_secure_version_on = utils.extract_query_parameters(request)
    parcel_stores = db.get_parcel_stores(
        address_search_phrase=address_search_phrase,
        is_secure_version_on=is_secure_version_on,
    )
    return RouteResponse(status_code=200, body=json.dumps(parcel_stores))


router = Router()
router.add_route(
    Route(
        path="/api/demo/sql-injection/parcel-stores",
        method="GET",
        handler=get_parcel_stores,
    )
)


def lambda_handler(event: LambdaEvent, context: LambdaContext) -> LambdaResponse:
    return router(event)
