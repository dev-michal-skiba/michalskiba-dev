from core.api import (
    HttpException,
    LambdaEvent,
    Route,
    Router,
    RouteRequest,
    RouteResponse,
)


class TestRouter:
    def test_route_exists(self) -> None:
        router = Router()
        router.add_route(
            Route(
                path="/",
                method="GET",
                handler=lambda request: RouteResponse(status_code=200),
            )
        )
        event: LambdaEvent = {
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                }
            }
        }

        response = router(event)

        assert response == {"statusCode": 200}

    def test_route_does_not_exist(self) -> None:
        router = Router()
        event: LambdaEvent = {
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                }
            }
        }

        response = router(event)

        assert response == {"statusCode": 404}

    def test_route_with_exception(self) -> None:
        def route_handler(request: RouteRequest) -> RouteResponse:
            raise HttpException(status_code=400, detail="Bad Request")

        router = Router()
        router.add_route(Route(path="/", method="GET", handler=route_handler))
        event: LambdaEvent = {
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                }
            }
        }

        response = router(event)

        assert response == {"statusCode": 400, "body": '{"detail": "Bad Request"}'}

    def test_get_request(self) -> None:
        router = Router()
        event: LambdaEvent = {
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                }
            },
            "queryStringParameters": {
                "param_1": "value_1",
                "param_2": "value_2",
            },
            "body": "{}",
            "headers": {
                "Host": "value_1",
                "X-Forwarded-Host": "value_2",
            },
        }

        response = router._get_request(event)

        assert response == RouteRequest(
            query_paramaters={"param_1": "value_1", "param_2": "value_2"},
            body="{}",
            headers={"host": "value_1", "x-forwarded-host": "value_2"},
        )
