from unittest.mock import Mock, patch

from core.api import RouteRequest
from sql_injection.lambda_function import lambda_handler


@patch("sql_injection.lambda_function.utils.extract_query_parameters")
@patch("sql_injection.lambda_function.db.get_parcel_stores")
class TestLambdaHandler:
    def test_lambda_handler(
        self, mock_get_parcel_stores: Mock, mock_extract_query_parameters: Mock
    ) -> None:
        address_search_phrase = "test address search phrase"
        is_secure_version_on = True
        mock_extract_query_parameters.return_value = address_search_phrase, is_secure_version_on
        parcel_stores = [
            {
                "name": "parcel_store_1",
                "address": "Red Street 1, 00-001 Warsaw, Poland",
                "opening_hours": "8:00-18:00",
                "access_code": "743763",
            }
        ]
        mock_get_parcel_stores.return_value = parcel_stores
        event = {
            "queryStringParameters": {"address_search_phrase": "Warsaw"},
            "requestContext": {
                "http": {
                    "method": "GET",
                    "path": "/api/demo/sql-injection/parcel-stores",
                }
            },
        }
        request = RouteRequest(query_paramaters={"address_search_phrase": "Warsaw"})

        response = lambda_handler(event, context={})

        assert response == {
            "statusCode": 200,
            "body": '{"parcel_stores": [{"name": "parcel_store_1", "address": "Red Street 1, 00-001 Warsaw, Poland", "opening_hours": "8:00-18:00", "access_code": "743763"}]}',
        }
        mock_extract_query_parameters.assert_called_once_with(request)
        mock_get_parcel_stores.assert_called_once_with(
            address_search_phrase=address_search_phrase,
            is_secure_version_on=is_secure_version_on,
        )
