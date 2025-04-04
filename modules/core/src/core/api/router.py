from typing import Callable

from .domain import HttpMethod, LambdaContext, LambdaEvent, LambdaResponse
from .exception import HttpException, NotFoundException


class Route:
    def __init__(
        self,
        path: str,
        method: HttpMethod,
        handler: Callable[[LambdaEvent, LambdaContext], LambdaResponse],
    ):
        self.path = path
        self.method = method
        self.handler = handler


class Router:
    def __init__(self) -> None:
        self.__routes: list[Route] = []

    def add_route(self, route: Route) -> None:
        self.__routes.append(route)

    def __call__(self, event: LambdaEvent, context: LambdaContext) -> LambdaResponse:
        path = event["requestContext"]["http"]["path"]
        method = event["requestContext"]["http"]["method"]
        try:
            for route in self.__routes:
                if route.path == path and route.method == method:
                    return route.handler(event, context)
        except HttpException as e:
            return e.response()
        return NotFoundException().response()
