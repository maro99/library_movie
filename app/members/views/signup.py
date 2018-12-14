from django.contrib.auth import get_user_model, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


import traceback
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from requests import Response
from members.tokens import account_activation_token

User = get_user_model()
from ..tasks import send_email

def signup(request):


    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        phone_number = request.POST['phone_number']
        user = User.objects.create_user(username=username,email=email,
                                        phone_number=phone_number, password=password)
        user.is_active = False
        user.save()

        send_email.delay(user.pk)

        return render(request, 'members/email_sent_succeed.html')

    return render(request, 'members/signup.html')

def user_activate(request,uidb64,token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
        user = User.objects.get(pk=uid)

    except(TypeError. ValueError, OverflowError, User.DoesNotExist):
        user = None

    try:
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse(user.email+ '계정이 활성화 되었습니다.')
        else:
            return HttpResponse('만료된 링크입니다.')

    except Exception as e:
        print(traceback.format_exc())