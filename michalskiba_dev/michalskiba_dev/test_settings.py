from .settings import *  # noqa: F403

SECRET_KEY = "test-secret-key"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": f"{BASE_DIR}/db.sqlite3",  # noqa: F405
    },
    "web_parameter_tampering": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": f"{BASE_DIR}/wpt_db.sqlite3",  # noqa: F405
    },
}

BASE_STATIC_PATH = BASE_DIR / "test_static"  # noqa: F405
BLOG_POSTS_RAW_PATH = BASE_STATIC_PATH / "blog/raw"
BLOG_POSTS_PATH = BASE_STATIC_PATH / "blog/posts"
BLOG_POSTS_IMAGES_PATH = BASE_STATIC_PATH / "blog/images"
