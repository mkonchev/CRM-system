from django.apps import AppConfig


class WorkstatusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.workstatus'
    verbose_name = 'Статус работы'

    def ready(self):
        import apps.workstatus.signals  # noqa: F401
