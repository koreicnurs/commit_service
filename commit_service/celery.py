import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commit_service.settings')

app = Celery('commit_service')
app.conf.broker_url = 'redis://localhost:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'pars_gitlab_repositories_every_day': {
        'task': 'commits.tasks.parsing_gitlab_repositories',
        'schedule': crontab(minute=0, hour=10),
    },
    'pars_github_repositories_every_day': {
        'task': 'commits.tasks.parsing_github_repositories',
        'schedule': crontab(minute=0, hour=10),
    },
}
