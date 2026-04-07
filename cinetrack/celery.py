import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cinetrack.settings")

app = Celery("cinetrack")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
