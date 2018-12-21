# celery-beat
from __future__ import absolute_import, unicode_literals
import random

# Celery 사용 위한것
import sys

from config import celery_app
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token

from django.contrib.auth import get_user_model


from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from config.settings.base import SMS_API_KEY, SMS_API_SECRET



User = get_user_model()

@celery_app.task
def send_email(pk):


    RUNSERVER = '/home/nasanmaro/.local/share/virtualenvs/library_movie-hgMtabiI/bin/celery' in sys.argv
    if RUNSERVER:
        domain = "localhost:8000"
    else:
        domain = "maro5.com"


    user = User.objects.get(pk=pk)

    # current_site = get_current_site(self.context['request']
    message = render_to_string('members/account_activate_email.html', {
        'user': user,  # 생성한 사용자 객체
        'domain': domain, #localhost:8000', "maro5.com"  # 이거 추후에 배포시에는 바꿔줘야함 #########
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),  # 생성한 사용자 객체의 pk를 암호화한 값
        'token': account_activation_token.make_token(user)  # 생성한 사용자 객체를 통해 생성한 token값.
    })

    # 이메일 전송 과정
    mail_subject = '도서관 영화 정보 페이지 회원가입 인증'
    to_email = user.email
    # EmailMessaage(제목, 본문, 받는이)
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


@celery_app.task
def send_info_change_email(pk,send_number,changed_email=None):

    user = User.objects.get(pk=pk)

    # current_site = get_current_site(self.context['request']
    message = render_to_string('members/user_info_change_email.html', {
        'user': user,
        'send_number':send_number,
    })

    # 이메일 전송 과정
    mail_subject = '도서관 영화 정보 페이지 회원정보 변경 인증번호'
    to_email = user.email

    # 만약 이번 호출에 바뀐 이메일에 확인메일 보내야 한다면
    if changed_email:
        to_email = changed_email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()




@celery_app.task
def send_sms(pk, send_number,changed_phone_number):

    user = User.objects.get(pk=pk)
    if changed_phone_number:
        number = changed_phone_number
    else:
        number = user.phone_number

    message = render_to_string('members/user_info_change_email.html', {
        'user': user,
        'send_number':send_number,
    })


    # set api key, api secret
    api_key = SMS_API_KEY
    api_secret = SMS_API_SECRET
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['from'] = '01066511550' # Sender number
    params['text'] = str(message) # Message

    if isinstance(number, (list, tuple)):
        number = ','.join(number)

    params['to'] = str(number)  # Recipients Number '01000000000,01000000001'

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)




# celery-beat tutorial 따라한것.
@celery_app.task(name="sum_two_numbers")
def add(x, y):
    return x + y

@celery_app.task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total
