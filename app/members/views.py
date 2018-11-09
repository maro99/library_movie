import inspect
import sys

import django
from django.contrib.auth import get_user_model, login
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

    # access token 얻기

    code = request.GET.get('code')
    url = 'https://graph.facebook.com/v3.0/oauth/access_token'

    redirect_uri = 'https://maro5.com/members/facebook_login/'
    RUNSERVER = 'runserver' in sys.argv
    if RUNSERVER:
        redirect_uri = 'http://localhost:8000/members/facebook_login/'

    params = {
        'client_id':FACEBOOK_APP_ID,
        'redirect_uri':redirect_uri ,
        'client_secret':FACEBOOK_APP_SECRET_CODE,
        'code':code,
    }

    response = requests.get(url,params)
    response_dict = response.json()
    access_token = response_dict['access_token']






    # aceess token 검사 --> fb id등 정보 받기

    url = 'https://graph.facebook.com/debug_token'

    params = {
        'input_token':access_token,
        'access_token':'{}|{}'.format(
            FACEBOOK_APP_ID, FACEBOOK_APP_SECRET_CODE
        )
    }
    response = requests.get(url, params)

    # 위에서 받은 response중 이름등 추가적 가져오기 위해서 scope를 전달해 줘야 한다. ----> http에 추가해 놓았다.






    # GraphAPI를 통햬써 Facebook User정보 받아오기.
    url = 'https://graph.facebook.com/v3.0/me'

    params = {
        'fields':
            ','.join(['id', 'name', 'first_name', 'last_name', 'picture']),
        'access_token': access_token,
    }
    response = requests.get(url, params)
    response_dict = response.json()




    # 받아온 정보 중 회원가입에 필요한 요소들 꺼내기
    facebook_user_id = response_dict['id']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_img_profile = response_dict['picture']['data']['url']

    # 있으면 get없으면 create하고 True도 같이 반환 .
    user, user_created = User.objects.get_or_create(
        username = facebook_user_id,
        defaults = {
            'first_name': first_name,
            'last_name': last_name,
        }
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



def login_page(request):

    facebook_redirect_uri = 'https://maro5.com/members/facebook_login/'
    kakaotalk_redirect_uri = 'https://maro5.com/members/kakaotalk_login/'

    # 런서버 중이면 로컬 호스트로 redirect 시케겠다.
    RUNSERVER = 'runserver' in sys.argv
    if RUNSERVER:
        facebook_redirect_uri = 'http://localhost:8000/members/facebook_login/'
        kakaotalk_redirect_uri = 'http://localhost:8000/members/kakaotalk_login/'


    context = {"facebook_redirect_uri":facebook_redirect_uri,
               "kakaotalk_redirect_uri":kakaotalk_redirect_uri,
               "kakaotalk_rest_api_key": KAKAOTALK_REST_API_KEY,}



    return render(request, 'members/login.html',context =context)
