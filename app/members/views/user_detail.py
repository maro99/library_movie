import sys

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

import traceback
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from members.tasks import send_info_change_email, send_sms
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

    context = {
            "uid":None,
            "token":None,
            "password":None,
        }


    if request.method == 'POST':


        password = request.POST.get('password')
        password = urlsafe_base64_encode(force_bytes(password)).decode('utf-8')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
        random_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

        token = passwod_change_token.make_token(user,random_number)

        send_info_change_email.delay(user.pk, random_number)

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
            user.save()
            return render(request, 'members/user_info_change_succeed_page.html')
        else:
            return render(request, 'members/user_info_change_fail_page.html')

    except Exception as e:
        print(traceback.format_exc())





def user_email_change_page(request):

    user = request.user

    context = {
            "uid":None,
            "token":None,
            "email":None,
        }


    if request.method == 'POST':


        email = request.POST.get('email')
        changed_email = email
        email = urlsafe_base64_encode(force_bytes(email)).decode('utf-8')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
        random_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

        token = passwod_change_token.make_token(user,random_number)

        send_info_change_email.delay(user.pk, random_number,changed_email)

        context = {
            "uid":uid,
            "token":token,
            "email":email,
        }

    return render(request, 'members/email_change.html',context)


def user_email_change(request,uidb64,token,email):

    random_number = request.POST.get('send_number')

    try:
        uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
        email  = force_text(urlsafe_base64_decode(email.encode('utf-8')))
        user = User.objects.get(pk=uid)

    except(TypeError.ValueError, OverflowError, User.DoesNotExist):
        user = None

    try:
        if user is not None and passwod_change_token.check_token(user, token,random_number):
            user.email = email
            user.save()
            return render(request, 'members/user_info_change_succeed_page.html')
        else:
            return render(request, 'members/user_info_change_fail_page.html')

    except Exception as e:
        print(traceback.format_exc())







def user_phone_number_change_page(request):

    user = request.user

    context = {
            "uid":None,
            "token":None,
            "phone_number":None,
        }

    if request.method == 'POST':

        phone_number = request.POST.get('phone_number')
        changed_phone_number = phone_number
        phone_number = urlsafe_base64_encode(force_bytes(phone_number)).decode('utf-8')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
        random_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

        token = passwod_change_token.make_token(user,random_number)

        send_sms.delay(user.pk, random_number,changed_phone_number)

        context = {
            "uid":uid,
            "token":token,
            "phone_number":phone_number,
        }

    return render(request, 'members/phone_number_change.html',context)


def user_phone_number_change(request,uidb64,token,phone_number):

    random_number = request.POST.get('send_number')

    try:
        uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
        phone_number  = force_text(urlsafe_base64_decode(phone_number.encode('utf-8')))
        user = User.objects.get(pk=uid)

    except(TypeError.ValueError, OverflowError, User.DoesNotExist):
        user = None

    try:
        if user is not None and passwod_change_token.check_token(user, token,random_number):
            user.phone_number = phone_number
            user.save()
            return render(request, 'members/user_info_change_succeed_page.html')
        else:
            return render(request, 'members/user_info_change_fail_page.html')

    except Exception as e:
        print(traceback.format_exc())



