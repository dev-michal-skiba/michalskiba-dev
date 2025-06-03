import json
from typing import Callable

from ..logger import Logger, get_logger
from .domain import (
    AuthorizerResponse,
    HttpMethod,
    LambdaAuthorizerResponse,
    LambdaAuthorizerResponseContext,
    LambdaEvent,
    LambdaResponse,
    RouteRequest,
    RouteResponse,
)
from .exception import HttpException, NotFoundException


class Route:
    def __init__(
        self,
        handler: Callable[[RouteRequest], RouteResponse],
        path: str | None = None,
        method: HttpMethod | None = None,
    ):
        self.path = path
        self.method = method
        self.handler = handler


class AuthorizerRoute:
    def __init__(self, handler: Callable[[RouteRequest], AuthorizerResponse]):
        self.handler = handler


class Router:
    def __init__(self) -> None:
        self.__authorizer_route: AuthorizerRoute | None = None
        self.__routes: list[Route] = []

    def add_route(self, route: Route | AuthorizerRoute) -> None:
        if isinstance(route, AuthorizerRoute):
            assert self.__authorizer_route is None, "Authorizer route already exists"
            self.__authorizer_route = route
        else:
            self.__routes.append(route)

    def _get_request(self, event: LambdaEvent) -> RouteRequest:
        headers = event.get("headers") or {}
        headers = {k.lower(): v for k, v in headers.items()}
        cookies = {
            c[0]: c[1]
            for c in (cookie.split("=", 1) for cookie in event.get("cookies") or [])
            if len(c) == 2
        }
        try:
            authorizer_username = event["requestContext"]["authorizer"]["lambda"]["username"]  # type: ignore[typeddict-item]
        except KeyError:
            authorizer_username = None
        event_body = event.get("body")
        if event_body:
            try:
                body = json.loads(event_body)
                if not isinstance(body, dict):
                    raise HttpException(status_code=400, detail="Expected JSON dictionary in body")
            except json.JSONDecodeError:
                raise HttpException(status_code=400, detail="Invalid JSON body")
        else:
            body = {}
        return RouteRequest(
            query_paramaters=event.get("queryStringParameters") or {},
            body=body,
            headers=headers,
            cookies=cookies,
            authorizer_username=authorizer_username,
        )

    def __handle_route_request(
        self,
        handler: Callable[[RouteRequest], RouteResponse],
        request: RouteRequest,
        logger: Logger,
    ) -> LambdaResponse:
        logger.log(f"Route Request: {request.model_dump_json()}")
        route_response = handler(request)
        response = LambdaResponse(statusCode=route_response.status_code)
        if route_response.body:
            try:
                response["body"] = json.dumps(route_response.body)
            except TypeError:
                print(f"Failed to serialize response body: [{request}] [{route_response}]")
                raise HttpException(status_code=500, detail="Internal server error")
        if route_response.headers:
            response["headers"] = route_response.headers
        logger.log(f"Route Response: {route_response.model_dump_json()}")
        logger.log(f"Lambda Route Response: {json.dumps(response)}")
        return response

    def __handle_authorizer_request(
        self,
        handler: Callable[[RouteRequest], AuthorizerResponse],
        request: RouteRequest,
        logger: Logger,
    ) -> LambdaAuthorizerResponse:
        logger.log(f"Authorizer Request: {request.model_dump_json()}")
        authorizer_response = handler(request)
        logger.log(f"Authorizer Response: {authorizer_response.model_dump_json()}")
        response = LambdaAuthorizerResponse(isAuthorized=authorizer_response.is_authorized)
        if authorizer_response.username:
            response["context"] = LambdaAuthorizerResponseContext(
                username=authorizer_response.username
            )
        logger.log(f"Lambda Authorizer Response: {json.dumps(response)}")
        return response

    def __call__(self, event: LambdaEvent) -> LambdaResponse | LambdaAuthorizerResponse:
        path = event["requestContext"]["http"]["path"]
        method = event["requestContext"]["http"]["method"]
        logger = get_logger(keys=[path, method])
        logger.log(f"LambdaEvent: {json.dumps(event)}")
        try:
            request = self._get_request(event)
            if event.get("type") == "REQUEST":
                if self.__authorizer_route is None:
                    return NotFoundException().response()
                return self.__handle_authorizer_request(
                    self.__authorizer_route.handler, request, logger
                )
            for route in self.__routes:
                if route.path == path and route.method == method:
                    return self.__handle_route_request(route.handler, request, logger)
        except HttpException as e:
            return e.response()
        return NotFoundException().response()
