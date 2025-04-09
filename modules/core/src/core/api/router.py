from typing import Callable

from .domain import (
    HttpMethod,
    LambdaEvent,
    LambdaResponse,
    RouteRequest,
    RouteResponse,
)
from .exception import HttpException, NotFoundException


class Route:
    def __init__(
        self,
        path: str,
        method: HttpMethod,
        handler: Callable[[RouteRequest], RouteResponse],
    ):
        self.path = path
        self.method = method
        self.handler = handler


class Router:
    def __init__(self) -> None:
        self.__routes: list[Route] = []

    def add_route(self, route: Route) -> None:
        self.__routes.append(route)

    def _get_request(self, event: LambdaEvent) -> RouteRequest:
        headers = event.get("headers") or {}
        headers = {k.lower(): v for k, v in headers.items()}
        return RouteRequest(
            query_paramaters=event.get("queryStringParameters") or {},
            body=event.get("body") or "",
            headers=headers,
        )

    def __call__(self, event: LambdaEvent) -> LambdaResponse:
        path = event["requestContext"]["http"]["path"]
        method = event["requestContext"]["http"]["method"]
        try:
            for route in self.__routes:
                if route.path == path and route.method == method:
                    request = self._get_request(event)
                    route_response = route.handler(request)
                    response = LambdaResponse(statusCode=route_response.status_code)
                    if route_response.body:
                        response["body"] = route_response.body
                    return response
        except HttpException as e:
            return e.response()
        return NotFoundException().response()
