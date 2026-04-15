from django.apps import AppConfig


class WorkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.work'
    verbose_name = 'Работа'

    def ready(self):
        import apps.work.signals  # noqa: F401
