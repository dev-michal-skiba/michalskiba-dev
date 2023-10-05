import pytest

from sql_injection.models import ParcelStore


@pytest.mark.django_db(databases=["sql_injection"])
class TestParcelStore:
    def test_str(self) -> None:
        parcel_store = ParcelStore.objects.create(
            name="a",
            address="b",
            opening_hours="c",
            access_code="d",
        )

        assert str(parcel_store) == "a"
