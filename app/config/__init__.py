# from __future__ import absolute_import, unicode_literals
#
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
#
# # 이하dml  이 app이 장고가 실행될때 항상 import되도록 한다.
# # @shared_task 데코레이터가 이엡을 이용할 것이다.
#
# from .celery_setting import  app as celery_app
#
# __all__=('celery_app')

#위쪽은 우리 프로젝트에서 celelry +rabbitmq 하던것



#이하는 이번에 celelry+ redis하려고 경영학도 따라하는중.

from .tasks import app as celery_app

__all__ = ['celery_app']