import pytest
from core.api import (
    AuthorizerResponse,
    AuthorizerRoute,
    HttpException,
    LambdaAuthorizerResponse,
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

    def test_route_response_correctly_serialized(self) -> None:
        router = Router()
        router.add_route(
            Route(
                path="/",
                method="GET",
                handler=lambda request: RouteResponse(status_code=200, body={"a": 1}),
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

        assert response == {"statusCode": 200, "body": '{"a": 1}'}

    def test_route_response_returned_non_serializable_body(self) -> None:
        router = Router()
        router.add_route(
            Route(
                path="/",
                method="GET",
                handler=lambda request: RouteResponse(status_code=200, body={"a": object()}),
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

        assert response == {"statusCode": 500, "body": '{"detail": "Internal server error"}'}

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
            "body": '{"a": 1}',
            "headers": {
                "Host": "value_1",
                "X-Forwarded-Host": "value_2",
            },
            "cookies": ["cookie_1=value_1", "cookie_2=value_2"],
        }

        response = router._get_request(event)

        assert response == RouteRequest(
            query_paramaters={"param_1": "value_1", "param_2": "value_2"},
            body={"a": 1},
            headers={"host": "value_1", "x-forwarded-host": "value_2"},
            cookies={"cookie_1": "value_1", "cookie_2": "value_2"},
        )

    def test_get_request_for_missing_body(self) -> None:
        router = Router()
        event: LambdaEvent = {}

        response = router._get_request(event)

        assert response.body == {}

    def test_get_request_for_invalid_json_body(self) -> None:
        router = Router()
        event: LambdaEvent = {
            "body": "{1: 'a'}",
        }

        with pytest.raises(HttpException) as e:
            router._get_request(event)

        assert e.value.status_code == 400
        assert e.value.detail == "Invalid JSON body"

    def test_get_request_for_json_body_but_not_dict(self) -> None:
        router = Router()
        event: LambdaEvent = {
            "body": "[1, 2, 3]",
        }

        with pytest.raises(HttpException) as e:
            router._get_request(event)

        assert e.value.status_code == 400
        assert e.value.detail == "Expected JSON dictionary in body"

    @pytest.mark.parametrize(
        "authorizer_response, expected_response",
        (
            (
                AuthorizerResponse(is_authorized=True, username="test"),
                {"isAuthorized": True, "context": {"username": "test"}},
            ),
            (AuthorizerResponse(is_authorized=False), {"isAuthorized": False}),
        ),
    )
    def test_authorizer_route_exists(
        self, authorizer_response: AuthorizerResponse, expected_response: LambdaAuthorizerResponse
    ) -> None:
        router = Router()
        router.add_route(AuthorizerRoute(handler=lambda request: authorizer_response))
        router.add_route(
            Route(path="/", method="GET", handler=lambda request: RouteResponse(status_code=200))
        )
        event: LambdaEvent = {
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                }
            },
            "type": "REQUEST",
        }

        response = router(event)

        assert response == expected_response

    def test_authorizer_route_does_not_exist(self) -> None:
        router = Router()
        event: LambdaEvent = {
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                }
            },
            "type": "REQUEST",
        }

        response = router(event)

        assert response == {"statusCode": 404}

    def test_authorizer_route_with_exception(self) -> None:
        def authorizer_handler(request: RouteRequest) -> AuthorizerResponse:
            raise HttpException(status_code=400, detail="Bad Request")

        router = Router()
        router.add_route(AuthorizerRoute(handler=authorizer_handler))
        router.add_route(
            Route(path="/", method="GET", handler=lambda request: RouteResponse(status_code=200))
        )
        event: LambdaEvent = {
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/",
                }
            },
            "type": "REQUEST",
        }

        response = router(event)

        assert response == {"statusCode": 400, "body": '{"detail": "Bad Request"}'}

    def test_second_authorizer_route_added(self) -> None:
        router = Router()
        router.add_route(
            AuthorizerRoute(handler=lambda request: AuthorizerResponse(is_authorized=False))
        )

        with pytest.raises(AssertionError) as e:
            router.add_route(
                AuthorizerRoute(handler=lambda request: AuthorizerResponse(is_authorized=False))
            )

        assert str(e.value) == "Authorizer route already exists"
