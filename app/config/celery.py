"""
셀러리를 장고 프로그램과 같이 사용하기 위해서는
Celery 라이브러리의 객체를 정의해야 한다 ---->이것을 app이라 부른다.   이하.

"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program
# 셀러리 프로그램을 위한 장고 셋팅 모듈을 설정한다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# 여기서사용되는 String 은
# worker가 환경 객체(configuration object)를
# 자식 process들에게 직렬화 시킬 필요 없다는 것을 의미한다.
# namespace = 'CELERY'는 celery와 완련된 모든 환경 키는 CELERY 접두사를 가져야 한다는걸 의미한다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
"""
app정의 다 했으면   

이 app을 DJango가 시작될때 load되도록 해야한다. --->__init__에 작성. 
해놓으면 
@shared_task 데코레이터가 이엡을 이용할 것이다. 
"""