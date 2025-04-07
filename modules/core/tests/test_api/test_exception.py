from core.api import HttpException, NotFoundException


class TestHttpException:
    def test_with_detail(self) -> None:
        exception = HttpException(status_code=400, detail="Bad Request")

        response = exception.response()

        assert response == {"statusCode": 400, "body": '{"detail": "Bad Request"}'}

    def test_without_detail(self) -> None:
        exception = HttpException(status_code=400)

        response = exception.response()

        assert response == {"statusCode": 400}


class TestNotFoundException:
    def test_response(self) -> None:
        exception = NotFoundException()

        response = exception.response()

        assert response == {"statusCode": 404}
