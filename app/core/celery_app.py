import os
from celery import Celery

celery_app = Celery(
    "task_service",
    broker=os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "rpc://"),
    include=["app.core.tasks"]
)

celery_app.autodiscover_tasks(["app"])

celery_app.conf.beat_schedule = {
    "process-pending-tasks-every-10-seconds": {
        "task": "app.core.tasks.process_pending_tasks",
        "schedule": 10.0,
    },
}

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)