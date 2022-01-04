import os
from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "my_property_solutions.settings"
)

app = Celery("my_property_solutions")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
