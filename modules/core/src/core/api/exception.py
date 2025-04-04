import json

from .domain import LambdaResponse


class HttpException(Exception):
    def __init__(self, *, status_code: int, detail: str | None = None):
        self.__status_code = status_code
        self.__detail = detail

    def response(self) -> LambdaResponse:
        response = LambdaResponse(statusCode=self.__status_code)
        if self.__detail:
            response["body"] = json.dumps({"detail": self.__detail})
        return response


class NotFoundException(HttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404)
