import os
from celery import Celery
from config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{settings.CELERY_MAIN}.settings")

app = Celery(
    settings.CELERY_MAIN,
    broker=settings.REDIS_URL,
    backend="rpc://",
    include=[f"{settings.CELERY_MAIN}.tasks"],
)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks([settings.CELERY_MAIN])
