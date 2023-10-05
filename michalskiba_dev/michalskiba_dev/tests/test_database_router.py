import pytest
from django.db.models import Model

from blog.models import BlogPost
from michalskiba_dev.database_router import DatabaseRouter
from sql_injection.models import ParcelStore
from web_parameter_tampering.models import PressApplication


@pytest.fixture
def database_router() -> DatabaseRouter:
    return DatabaseRouter()


class TestDatabaseRouter:
    class TestDbForRead:
        @pytest.mark.parametrize(
            "model, expected_database",
            ((BlogPost, None), (PressApplication, None), (ParcelStore, "sql_injection")),
        )
        def test_expected_database(
            self, database_router: DatabaseRouter, model: Model, expected_database: str | None
        ) -> None:
            db_for_read = database_router.db_for_read(model)

            assert db_for_read == expected_database

    class TestDbForWrite:
        @pytest.mark.parametrize(
            "model, expected_database",
            ((BlogPost, None), (PressApplication, None), (ParcelStore, "sql_injection")),
        )
        def test_expected_database(
            self, database_router: DatabaseRouter, model: Model, expected_database: str | None
        ) -> None:
            db_for_write = database_router.db_for_write(model)

            assert db_for_write == expected_database

    class TestAllowRelation:
        def test_always_defaults_to_disallow_cross_database_relations(
            self, database_router: DatabaseRouter
        ) -> None:
            allow_relation = database_router.allow_relation(obj1=None, obj2=None)
            assert allow_relation is None

    class TestAllowMigrate:
        def test_allow_for_table_in_default_database_when_migrating_for_default_database(
            self, database_router: DatabaseRouter
        ) -> None:
            allow_migrate = database_router.allow_migrate(db="default", app_label="blog")

            assert allow_migrate is True

        @pytest.mark.parametrize("db", ("sql_injection",))
        def test_disallow_for_table_in_default_database_when_migrating_for_non_default_database(
            self, database_router: DatabaseRouter, db: str
        ) -> None:
            allow_migrate = database_router.allow_migrate(db=db, app_label="blog")

            assert allow_migrate is False

        @pytest.mark.parametrize("db, app_label", (("sql_injection", "sql_injection"),))
        def test_allow_for_table_in_non_default_database_when_migrating_for_non_default_database(
            self, database_router: DatabaseRouter, db: str, app_label: str
        ) -> None:
            allow_migrate = database_router.allow_migrate(db=db, app_label=app_label)

            assert allow_migrate is True

        @pytest.mark.parametrize("app_label", ("sql_injection",))
        def test_disallow_for_table_in_non_default_database_when_migrating_for_default_database(
            self, database_router: DatabaseRouter, app_label: str
        ) -> None:
            allow_migrate = database_router.allow_migrate(db="default", app_label=app_label)

            assert allow_migrate is False
