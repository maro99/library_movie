from django.contrib.auth import get_user_model, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


import traceback
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from requests import Response

from members.forms import SignupForm
from members.tokens import account_activation_token

User = get_user_model()
from ..tasks import send_email

def signup(request):

    if request.method =='POST':

        form = SignupForm(request.POST)

        # form에 들어있는 데이터가 유효한지 검사.(해당 form 클래스에서 정의한 데이터 형식에서 벋어나지 않는지 판단.)
        if form.is_valid():

            user = form.signup() #signup 메소드는 form의 메소드 인데 form은 signupForm클래스의 인스턴스이다.

            user.is_active = False
            user.save()

            send_email.delay(user.pk)

            return render(request, 'members/email_sent_succeed.html')

    else:
        form = SignupForm()

    context = {'form': form, }
    return render(request, 'members/signup.html', context)


def user_activate(request,uidb64,token):

    try:
        # uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ {uid}')
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