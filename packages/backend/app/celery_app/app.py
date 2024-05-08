import os
import redis
from celery import Celery

REDIS_BROKER = os.getenv("REDIS_BROKER", "redis://redis:6379/0")

r = redis.Redis.from_url(REDIS_BROKER)
app = Celery("callmates-tasks", broker=REDIS_BROKER)

# set the configuration for the celery app
app.conf.update(
    task_acks_late=True,  # This will make sure that the task is not acknowledged until the task is completed
    task_reject_on_worker_lost=True,  # This will make sure that the task is not lost if the worker is lost
)
app.conf.result_backend = REDIS_BROKER  # type: ignore
