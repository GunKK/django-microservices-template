import os

from celery import Celery

CELERY_BROKER_URL = os.getenv("CELERY_REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_REDIS_URL", "redis://localhost:6379/0")

celery_client = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)
