import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.timezone = os.environ.get("TIMEZONE", default="UTC")
# app.conf.beat_schedule = {
#     'test_long_task': {
#         'task': 'apps.order.tasks.test_chrone_task',
#         'schedule': 10.0
#     }
# }
