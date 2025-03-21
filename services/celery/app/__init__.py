from .celery import app as celery_worker

__all__ = ["celery_worker"]
