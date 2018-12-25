#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# 문자열로 등록한 이유는 Celery Worker가 자식 프로세스에게 configuration object를 직렬화하지 않아도 된다는것 때문
# namespace = 'CELERY'는 모든 celery 관련한 configuration key가 'CELERY_' 로 시작해야함을 의미함
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# celery-beat tutorial보고 추가.
from celery.schedules import crontab

app.conf.beat_schedule = {
    # 'add-every-minute-contrab': {
    #     'task': 'multiply_two_numbers',
    #     'schedule': crontab(),  # 1분마다
    #     'args': (16, 16),
    # },
    # 'add-every-5-seconds': {
    #     'task': 'sum_two_numbers',
    #     'schedule': 5.0,  # 5초마다
    #     'args': (16,16)
    # },
    # 'add-every-30-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': 30.0, # 30초마다
    #     'args': (16, 16)
    # },
    'add-every-minute-contrab': {
        'task': 'crawling_then_send_result_email',
        'schedule': crontab(minute=52, hour=0),
        'args': (),
    },
}