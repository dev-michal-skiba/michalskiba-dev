from typing import Literal, NotRequired, TypedDict

from pydantic import BaseModel

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


class LambdaHttp(TypedDict):
    method: HttpMethod
    path: str


class Lambda(TypedDict):
    username: NotRequired[str]


class LambdaAuthorizer(TypedDict):
    lambda: NotRequired[Lambda]  # type: ignore[misc]


class LambdaRequestContext(TypedDict):
    http: LambdaHttp
    authorizer: NotRequired[LambdaAuthorizer]


class LambdaEvent(TypedDict):
    requestContext: LambdaRequestContext
    queryStringParameters: NotRequired[dict[str, str]]
    body: NotRequired[str]
    headers: NotRequired[dict[str, str]]
    cookies: NotRequired[list[str]]
    type: NotRequired[str]


class LambdaContext(TypedDict):
    pass


class LambdaResponse(TypedDict):
    statusCode: int
    body: NotRequired[str]
    headers: NotRequired[dict[str, str]]


class LambdaAuthorizerResponseContext(TypedDict):
    username: str


class LambdaAuthorizerResponse(TypedDict):
    isAuthorized: bool
    context: NotRequired[LambdaAuthorizerResponseContext]


class RouteRequest(BaseModel):
    body: str = ""
    headers: dict[str, str] = {}
    cookies: dict[str, str] = {}
    query_paramaters: dict[str, str] = {}
    authorizer_username: str | None = None


class RouteResponse(BaseModel):
    status_code: int
    body: str | None = None
    headers: dict[str, str] | None = None


class AuthorizerResponse(BaseModel):
    is_authorized: bool
    username: str | None = None
