from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.order'
    verbose_name = 'Заявка'

    def ready(self):
        import apps.order.signals  # noqa: F401
