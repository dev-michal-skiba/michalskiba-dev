from typing import Literal, NotRequired, TypedDict

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
