from typing import Any

from django.conf import settings
from django.db.models import Model


class DatabaseRouter:
    def db_for_read(self, model: Model, **hints: dict[Any, Any]) -> str | None:
        """
        If app has dedicated database, use the dedicated database,
        if not, use default database
        """
        if model._meta.app_label in settings.APPS_WITH_DEDICATED_DATABASE:
            return model._meta.app_label
        return None

    def db_for_write(self, model: Model, **hints: dict[Any, Any]) -> str | None:
        """
        If app has dedicated database, use the dedicated database,
        if not, use default database
        """
        if model._meta.app_label in settings.APPS_WITH_DEDICATED_DATABASE:
            return model._meta.app_label
        return None

    def allow_relation(self, obj1: Any, obj2: Any, **hints: dict[Any, Any]) -> bool | None:
        """
        Allow relations only if tables are in the same database
        """
        return None

    def allow_migrate(
        self, db: str, app_label: str, model_name: str | None = None, **hints: dict[Any, Any]
    ) -> bool | None:
        """
        For migrations from apps with dedicated database, allow migrations only on that database,
        for other migrations, allow migrations only in default database
        """
        if app_label in settings.APPS_WITH_DEDICATED_DATABASE:
            return db == app_label
        return db == "default"
