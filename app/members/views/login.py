import inspect
import sys

import django
from django.contrib.auth import get_user_model, login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect

import requests

# Create your views here.
import members
from config.settings.base import *
User = get_user_model()


def normal_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

    return redirect('main_page')

def facebook_login(request):

    code = request.GET.get('code')
    user = authenticate(request, code=code)

    if user is not None:
        login(request, user)

    return redirect('main_page')

def kakaotalk_login(request):

    code = request.GET.get('code')
    user = authenticate(request, code=code)

    if user is not None:
        login(request, user)

    return redirect('main_page')

def naver_login(request):

    # 1. code 받기
    code = request.GET.get('code')
    state = request.GET.get('state')
    user = authenticate(request, code=code,state=state)

    if user is not None:
        login(request, user)

    return redirect('main_page')

def google_login(request):

    code = request.GET.get('code')
    user = authenticate(request, code=code)

    if user is not None:
        login(request, user)

    return redirect('main_page')

def login_page(request):

    # 런서버 중이면 로컬 호스트로 redirect 시케겠다.
    RUNSERVER = 'runserver' in sys.argv
    if RUNSERVER:
        facebook_redirect_uri = 'http://localhost:8000/members/facebook_login/'
        kakaotalk_redirect_uri = 'http://localhost:8000/members/kakaotalk_login/'
        naver_redirect_uri = 'http://localhost:8000/members/naver_login/'
        google_redirect_uri = 'http://localhost:8000/members/google_login/'
    else:
        facebook_redirect_uri = 'https://maro5.com/members/facebook_login/'
        kakaotalk_redirect_uri = 'https://maro5.com/members/kakaotalk_login/'
        naver_redirect_uri = 'https://maro5.com/members/naver_login/'
        google_redirect_uri = 'https://maro5.com/members/google_login/'

    context = {"facebook_redirect_uri":facebook_redirect_uri,
               "fecebook_app_id":FACEBOOK_APP_ID,
               "kakaotalk_redirect_uri":kakaotalk_redirect_uri,
               "kakaotalk_rest_api_key": KAKAOTALK_REST_API_KEY,
               "naver_redirect_uri": naver_redirect_uri,
               "naver_client_id": NAVER_CLIENT_ID,
                "google_client_id": GOOGLE_CLIENT_ID,
               "google_redirect_uri":google_redirect_uri
               }



    return render(request, 'members/login.html',context =context)
