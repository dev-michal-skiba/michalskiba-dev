from django.apps import AppConfig


class SqlInjectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sql_injection"
