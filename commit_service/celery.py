import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commit_service.settings')

app = Celery('commit_service')
app.conf.broker_url = 'redis://localhost:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'pars_repositories_every_day': {
        'task': 'commits.tasks.parsing_repositories',
        'schedule': crontab(),
    },
}
