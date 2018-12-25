# celery-beat
from __future__ import absolute_import, unicode_literals

import datetime
from config import celery_app
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model

from movies.models import District

from movies.utils import *

User = get_user_model()

@celery_app.task(name="crawling_then_send_result_email")
def crawling_then_send_result_email():

    # 지역 없으면 지역정보 부터 업데이트
    if District.objects.all() == None:
        get_info()

    # 영화 크롤링
    dict_log_result = main_movie_crawler()

    message = render_to_string('movie/daily_crawling_result_mail_form.html', {
        'dict_log': dict_log_result
    })

    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # 이메일 전송 과정
    mail_subject = f"{now_date} 크롤링 결과 보고"
    to_email = "nadcdc4@gmail.com"
    # EmailMessaage(제목, 본문, 받는이)
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

