# celery-beat
from __future__ import absolute_import, unicode_literals
import random

# Celery 사용 위한것
from config import celery_app
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token

from django.contrib.auth import get_user_model


User = get_user_model()

@celery_app.task
def send_email(pk):

    user = User.objects.get(pk=pk)

    # current_site = get_current_site(self.context['request']
    message = render_to_string('members/account_activate_email.html', {
        'user': user,  # 생성한 사용자 객체
        'domain': 'maro5.com', #localhost:8000',  # 이거 추후에 배포시에는 바꿔줬던것 같다? #########
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),  # 생성한 사용자 객체의 pk를 암호화한 값
        'token': account_activation_token.make_token(user)  # 생성한 사용자 객체를 통해 생성한 token값.
    })

    # 이메일 전송 과정
    mail_subject = 'test'
    to_email = user.email
    # EmailMessaage(제목, 본문, 받는이)
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


# celery-beat tutorial 따라한것.
@celery_app.task(name="sum_two_numbers")
def add(x, y):
    return x + y

@celery_app.task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total
