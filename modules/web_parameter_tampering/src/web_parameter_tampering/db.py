from typing import cast

from core.db import BaseDatabaseModel, CharField


class PressApplication(BaseDatabaseModel):
    username: CharField = CharField(max_length=32, unique=True)
    organization: CharField = CharField(max_length=64)
    accreditation_code: CharField = CharField(max_length=36, null=True)


def get_press_application(username: str) -> PressApplication | None:
    try:
        return cast(PressApplication, PressApplication.get(PressApplication.username == username))
    except PressApplication.DoesNotExist:
        return None
