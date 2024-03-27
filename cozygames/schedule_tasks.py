from celery import shared_task


@shared_task()
def daily_task_test():
    print("\033[33mINFO:\033[0m SCHEDULE TASK FROM CELERY")
    return "\033[33mINFO:\033[0m RETURN SCHEDULE TASK FROM CELERY"
