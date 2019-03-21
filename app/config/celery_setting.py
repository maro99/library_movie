#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals
import os
import sys

from celery import Celery

# set the default Django settings module for the 'celery' program

# 설정 파일 변경 위한것.
# 이부분 local때 잘 적용되는지 테스트 안해봤으니
# dev모드, local에서 if안으로 잘 들어가나보자. -> 잘안되면 redis가 local이 아닐 것임.
if '/home/nasanmaro/.local/share/virtualenvs/library_movie-hgMtabiI/bin/celery' in sys.argv:
    setting_file = 'config.settings.local'
else:
    setting_file = 'config.settings.production'



os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_file)

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
    'add-every-hour-contab': {
        'task': 'send_alarm_email',
        'schedule': crontab(minute=0, hour='*/1'),
        # 'schedule': crontab(minute=34, hour=21),
        # 'schedule': 30.0,  # 5초마다
        'args': ()
    },
    'add-every-minute-contrab': {
        'task': 'crawling_then_send_result_email',
        'schedule': crontab(minute=26, hour=21),
        'args': (),
    },
}