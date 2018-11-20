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
        return render(request, 'normal_login_succed.html')

    else:
        return render(request,'members/login.html')


def facebook_login(request):

    code = request.GET.get('code')
    user = authenticate(request, code=code)

    if user is not None:
        login(request, user)
        # 어떤 함수 테스트 중인지도 전달해 주겠다.
        frame = inspect.currentframe()
        function_name = inspect.getframeinfo(frame).function
        context = {'function_name': function_name}

        return render(request,'social_login_succed.html',context)

    return redirect('login_page')




def kakaotalk_login(request):

    # 1. code 받기
    code = request.GET.get('code')
    # return HttpResponse(code)


    # 2 .access token 받기
    url = "https://kauth.kakao.com/oauth/token"
    kakaotalk_redirect_uri = 'https://maro5.com/members/kakaotalk_login/'

    RUNSERVER = 'runserver' in sys.argv
    if RUNSERVER:
        kakaotalk_redirect_uri = 'http://localhost:8000/members/kakaotalk_login/'

    params = {
        'grant_type':'authorization_code',
        'client_id':KAKAOTALK_REST_API_KEY,
        'redirect_uri':kakaotalk_redirect_uri,
        'code':code
    }

    response = requests.post(url,params)
    response_dict = response.json()
    access_token = response_dict['access_token']
    # return HttpResponse(access_token)


    # 3. access token 이용해서 app loigin
    # 엡연결-로긴 은 로그인한 사용자와 앱을 카카오 플랫폼에 연결함으로서
    # 일반적인 사용자가 앱 가입/등록 요청을 하는 경우와 비슷하다.
    # 카카오 서비스 이용하기 위해서 로그인 후 앱연결 선행되야 하고 앱연결 올바로 수행되면 사용자대한 고유한 아이디 부여된다.
    url = "https://kapi.kakao.com/v1/user/signup"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
    }
    headers.update({'Authorization':'Bearer ' + str(access_token)})
    response = requests.post(url, headers=headers)
    # return HttpResponse(response)


    # 4. acces _token 이용해서 사용자 정보 요청.
    # 사용자의 id, 카카오 계정 email 및 상세정보 얻어올 수 있는 기능.
    # 사용자 로그인 후 얻은 사용자토큰, 엡연결이 되어있어야 한다.
    url = "https://kapi.kakao.com/v1/user/me"
    response = requests.post(url, headers=headers)
    # return HttpResponse(response)

    response_dict = response.json()

    #5. 받아온 정보 중 회원가입에 필요한 요소들 꺼내기 및 회원 가입
    id = response_dict['id']
    email = response_dict['kaccount_email']
    nickname = response_dict['properties']['nickname']
    url_img_profile = response_dict['properties']['profile_image']#['url']

    # 있으면 get없으면 create하고 True도 같이 반환 .
    user, user_created = User.objects.get_or_create(
        username = id,
        email = email,
    )

    login(request, user,backend='django.contrib.auth.backends.ModelBackend')

    # return redirect('index')

    if user is not None:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # 어떤 함수 테스트 중인지도 전달해 주겠다.
        frame = inspect.currentframe()
        function_name = inspect.getframeinfo(frame).function
        context = {'function_name': function_name}

        return render(request,'social_login_succed.html',context)

    return redirect('login_page')



def naver_login(request):

    # 1. code 받기
    code = request.GET.get('code')
    state = request.GET.get('state')
    # return HttpResponse(state)


    # 2 .access token 받기
    url = "https://nid.naver.com/oauth2.0/token"
    naver_redirect_uri = 'https://maro5.com/members/kakaotalk_login/'

    RUNSERVER = 'runserver' in sys.argv
    if RUNSERVER:
        naver_redirect_uri = 'http://localhost:8000/members/kakaotalk_login/'

    params = {
        'grant_type':'authorization_code',
        'client_id':NAVER_CLIENT_ID,
        'client_secret':NAVER_CLIENT_SECRET,
        'redirect_uri':naver_redirect_uri,
        'code':code,
        'state':state
    }

    response = requests.post(url,params)
    response_dict = response.json()
    access_token = response_dict['access_token']
    # return HttpResponse(access_token)

    #
    # # 3. access token 이용해서 회원프로필 조회
    url = "https://openapi.naver.com/v1/nid/me"
    headers = {
        'Authorization': 'Bearer ' + str(access_token)
    }
    response = requests.post(url, headers=headers)
    # return HttpResponse(response)

    response_dict = response.json()

    #4. 받아온 정보 중 회원가입에 필요한 요소들 꺼내기 및 회원 가입
    id = response_dict['response']['id']
    email = response_dict['response']['email']

    # 있으면 get없으면 create하고 True도 같이 반환 .
    user, user_created = User.objects.get_or_create(
        username = id,
        email = email,
    )

    login(request, user,backend='django.contrib.auth.backends.ModelBackend')

    # return redirect('index')

    if user is not None:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # 어떤 함수 테스트 중인지도 전달해 주겠다.
        frame = inspect.currentframe()
        function_name = inspect.getframeinfo(frame).function
        context = {'function_name': function_name}

        return render(request,'social_login_succed.html',context)

    return redirect('login_page')


def google_login(request):

    # 1. access token 얻기

    code = request.GET.get('code')
    # return HttpResponse(code)

    url = 'https://www.googleapis.com/oauth2/v4/token'

    redirect_uri = 'https://maro5.com/members/google_login/'
    RUNSERVER = 'runserver' in sys.argv
    if RUNSERVER:
        redirect_uri = 'http://localhost:8000/members/google_login/'

    params = {
        'grant_type': 'authorization_code',
        'client_id':GOOGLE_CLIENT_ID,
        'redirect_uri':redirect_uri ,
        'client_secret':GOOGLE_CLIENT_SECRET,
        'code':code,
    }

    response = requests.post(url,params)
    response_dict = response.json()
    access_token = response_dict['access_token']
    # return HttpResponse(access_token)



    # # 3. access token 이용해서 회원프로필 조회
    url = "https://www.googleapis.com/oauth2/v1/userinfo"

    params ={
        'access_token': access_token,'alt': 'json'
    }

    response = requests.get(url,params=params)
    # return HttpResponse(response)

    # {"id": "108743605198166301707", "name": "Sanmaro Na", "given_name": "Sanmaro", "family_name": "Na",
    #  "link": "https://plus.google.com/108743605198166301707",
    #  "picture": "https://lh6.googleusercontent.com/-cYOpZZldajQ/AAAAAAAAAAI/AAAAAAAABtw/q8-Hofd6_QY/photo.jpg",
    #  "gender": "male", "locale": "ko"}

    response_dict = response.json()



    # 4. 받아온 정보 중 회원가입에 필요한 요소들 꺼내기 및 회원 가입
    id = response_dict['id']
    given_name = response_dict['given_name']
    family_name = response_dict['family_name']

    # 있으면 get없으면 create하고 True도 같이 반환 .
    user, user_created = User.objects.get_or_create(
        username=id,
        defaults={
            'first_name': given_name,
            'last_name': family_name,
        }
    )

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    # return redirect('index')

    if user is not None:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # 어떤 함수 테스트 중인지도 전달해 주겠다.
        frame = inspect.currentframe()
        function_name = inspect.getframeinfo(frame).function
        context = {'function_name': function_name}

        return render(request, 'social_login_succed.html', context)

    return redirect('login_page')


def login_page(request):

    facebook_redirect_uri = 'https://maro5.com/members/facebook_login/'
    kakaotalk_redirect_uri = 'https://maro5.com/members/kakaotalk_login/'
    naver_redirect_uri = 'https://maro5.com/members/naver_login/'
    google_redirect_uri = 'https://maro5.com/members/google_login/'

    # 런서버 중이면 로컬 호스트로 redirect 시케겠다.
    RUNSERVER = 'runserver' in sys.argv
    if RUNSERVER:
        facebook_redirect_uri = 'http://localhost:8000/members/facebook_login/'
        kakaotalk_redirect_uri = 'http://localhost:8000/members/kakaotalk_login/'
        naver_redirect_uri = 'http://localhost:8000/members/naver_login/'
        google_redirect_uri = 'http://localhost:8000/members/google_login/'

    context = {"facebook_redirect_uri":facebook_redirect_uri,
               "kakaotalk_redirect_uri":kakaotalk_redirect_uri,
               "kakaotalk_rest_api_key": KAKAOTALK_REST_API_KEY,
               "naver_redirect_uri": naver_redirect_uri,
               "naver_client_id": NAVER_CLIENT_ID,
                "google_client_id": GOOGLE_CLIENT_ID,
               "google_redirect_uri":google_redirect_uri
               }



    return render(request, 'members/login.html',context =context)
