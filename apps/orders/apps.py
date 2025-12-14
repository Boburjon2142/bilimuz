<<<<<<< HEAD
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.orders"

    def ready(self):
        from . import signals  # noqa: F401
=======
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.orders"
>>>>>>> 93b4415ddc6ddc26ae88b35d34a582fb128c09c3
