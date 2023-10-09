from typing import Any

from django.db import migrations


def apply(apps: Any, schema_editor: Any) -> None:
    ParcelStore = apps.get_model("sql_injection", "ParcelStore")
    ParcelStore.objects.bulk_create(
        [
            ParcelStore(
                name="parcel_store_1",
                address="Red Street 1, 00-001 Warsaw, Poland",
                opening_hours="8:00-18:00",
                access_code="743763",
            ),
            ParcelStore(
                name="parcel_store_2",
                address="Blue Street 2, 47-404 Wroclaw, Poland",
                opening_hours="7:00-15:00",
                access_code="951620",
            ),
            ParcelStore(
                name="parcel_store_3",
                address="Green Street 3, 00-001 Warsaw, Poland",
                opening_hours="9:00-17:00",
                access_code="477584",
            ),
        ]
    )


def revert(apps: Any, schema_editor: Any) -> None:
    ParcelStore = apps.get_model("sql_injection", "ParcelStore")
    ParcelStore.objects.filter(
        name__in=["parcel_store_1", "parcel_store_2", "parcel_store_3"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("sql_injection", "0001_create_parcel_store"),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]
