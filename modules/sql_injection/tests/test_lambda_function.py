from unittest.mock import Mock, patch

from sql_injection.lambda_function import lambda_handler


@patch("sql_injection.lambda_function.get_address_search_phrase")
@patch("sql_injection.lambda_function.get_parcel_stores")
class TestLambdaHandler:
    def test_lambda_handler(
        self, mock_get_parcel_stores: Mock, mock_get_address_search_phrase: Mock, freeze_time: None
    ) -> None:

        address_search_phrase = "test address search phrase"
        mock_get_address_search_phrase.return_value = address_search_phrase
        parcel_stores = [
            {
                "name": "parcel_store_1",
                "address": "Red Street 1, 00-001 Warsaw, Poland",
                "opening_hours": "8:00-18:00",
                "access_code": "743763",
            }
        ]
        mock_get_parcel_stores.return_value = parcel_stores
        event = {"queryStringParameters": {"address_search_phrase": "Warsaw"}}
        context = {"id": "test context"}

        response = lambda_handler(event, context)

        assert response == {
            "statusCode": 200,
            "body": (
                '[{"name": "parcel_store_1", "address": "Red Street 1, 00-001 Warsaw, Poland", '
                '"opening_hours": "8:00-18:00", "access_code": "743763"}]'
            ),
            "headers": {
                "Set-Cookie": "is_secure_version_on=True; Expires=2025-04-08T12:00:00+00:00; Path=/; Secure"
            },
        }
        mock_get_address_search_phrase.assert_called_once_with(event)
        mock_get_parcel_stores.assert_called_once_with(
            address_search_phrase=address_search_phrase,
            is_secure_version_on=True,
        )
