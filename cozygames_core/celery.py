from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from . import settings

CELERY_TIMEZONE = 'Europe/Minsk'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cozygames_core.settings')

app = Celery('cozygames_core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)

# Schedule tasks
app.conf.beat_schedule = {
    'daily-task1': {
        'task': 'cozygames.schedule_tasks.daily_task_test',
        'schedule': 10,
    },
    # Other schedule tasks add here
}
