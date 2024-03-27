from celery import shared_task
from datetime import datetime
from celery import Celery


@shared_task()
def test_task():
    print("\033[33mINFO:\033[0m TASK FROM CELERY")
    print("Task from celery")
    return 'Return test_task'
