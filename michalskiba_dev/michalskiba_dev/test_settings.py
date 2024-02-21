from .settings import *  # noqa: F403

SECRET_KEY = "test-secret-key"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": f"{BASE_DIR}/db.sqlite3",  # noqa: F405
    },
    "sql_injection": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": f"{BASE_DIR}/sql_injection_db.sqlite3",  # noqa: F405
    },
}
