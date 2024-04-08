import pytest


@pytest.mark.freeze_time
@pytest.fixture
def freeze_time(freezer) -> None:  # type: ignore[no-untyped-def]
    freezer.move_to("2024-04-08 12:00:00.000000+00:00")
