import sys

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

import traceback
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from members.tasks import send_password_change_email
from members.tokens import passwod_change_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

import random
import string

User = get_user_model()

def user_detail_page(request):
    return render(request,'members/user_detail.html')


def user_info_change_page(request):
    return render(request, 'members/user_info_change.html')


def user_password_change_page(request):

    user = request.user

    context = None


    if request.method == 'POST':


        password = request.POST.get('password')
        password = urlsafe_base64_encode(force_bytes(password)).decode('utf-8')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
        random_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

        token = passwod_change_token.make_token(user,random_number)

        send_password_change_email.delay(user.pk, random_number)

        context = {
            "uid":uid,
            "token":token,
            "password":password,
        }

    return render(request, 'members/password_change.html',context)


def user_password_change(request,uidb64,token,password):

    random_number = request.POST.get('send_number')

    try:
        uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
        password  = force_text(urlsafe_base64_decode(password.encode('utf-8')))
        user = User.objects.get(pk=uid)

    except(TypeError.ValueError, OverflowError, User.DoesNotExist):
        user = None

    try:
        if user is not None and passwod_change_token.check_token(user, token,random_number):
            user.set_password(password)
            print(password)
            user.save()
            return HttpResponse(user.email + '비밀번호 변경이 완료되었습니다.')
        else:
            return HttpResponse('만료된 링크입니다.')

    except Exception as e:
        print(traceback.format_exc())
