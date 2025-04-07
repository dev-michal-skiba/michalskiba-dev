from typing import Literal, NotRequired, TypedDict

from pydantic import BaseModel

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


class LambdaHttp(TypedDict):
    method: HttpMethod
    path: str


class LambdaRequestContext(TypedDict):
    http: LambdaHttp


class LambdaEvent(TypedDict):
    requestContext: LambdaRequestContext
    queryStringParameters: NotRequired[dict[str, str]]


class LambdaContext(TypedDict):
    pass


class LambdaResponse(TypedDict):
    statusCode: int
    body: NotRequired[str]


class RouteRequest(BaseModel):
    query_paramaters: dict[str, str]


class RouteResponse(BaseModel):
    status_code: int
    body: str | None = None
