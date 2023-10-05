import pytest
from django.test import RequestFactory

from demo.constants import IS_SECURE_VERSION_ON_COOKIE_NAME
from sql_injection.views import home


@pytest.mark.django_db(databases=["sql_injection"])
class TestHome:
    @pytest.mark.parametrize("is_secure_version_on", ("False", "True"))
    def test_view_returns_correct_parcel_stores(self, is_secure_version_on: str) -> None:
        request = RequestFactory().get("/?address-search-phrase=Warsaw")
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = is_secure_version_on

        response = home(request, *[], **{})

        assert response.status_code == 200
        assert response.content.count(b"sql-injection-parcel-store-tile") == 2

    def test_view_returns_no_parcel_stores_for_sql_injection_and_secure_version(self) -> None:
        request = RequestFactory().get(
            "/?address-search-phrase=Warsaw%25%25%27+UNION+SELECT+NULL%2C+name%2C+address"
            "%2C+access_code+FROM+sql_injection_parcelstore%3B+--"
        )
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = "True"

        response = home(request, *[], **{})

        assert response.status_code == 200
        assert response.content.count(b"sql-injection-parcel-store-tile") == 0

    def test_view_returns_parcel_stores_for_sql_injection_and_insecure_version(self) -> None:
        request = RequestFactory().get(
            "/?address-search-phrase=Warsaw%25%25%27+UNION+SELECT+NULL%2C+name%2C+address"
            "%2C+access_code+FROM+sql_injection_parcelstore%3B+--"
        )
        request.COOKIES[IS_SECURE_VERSION_ON_COOKIE_NAME] = "False"

        response = home(request, *[], **{})

        assert response.status_code == 200
        assert response.content.count(b"sql-injection-parcel-store-tile") == 5
