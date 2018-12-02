
# admin /특정비밀번호
# 위 값으로 로그인 시도시 authenticate가 성송하도록 커스텀 Backend를 작성
# members.backends모듈에 작성
# Backend 명은 Settings.Backend
# password는 장고안의 문자열을 생성해서? 써야함.

import sys
import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from config.settings.base import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET_CODE, KAKAOTALK_REST_API_KEY

User = get_user_model()




class SettingsBackend:
    '''
        ADMIN = 'admin'
        ADMIN_PASSWORD ='pbkdf2_sha256$100000$zNIjdY5qwrae$dASPtmQ/vw7VQ9cFD69aYu7hTxTLQLoFFzLqUzxtq1I='
        '''

    def authenticate(self, request, username=None,password=None):
        login_valid = (settings.ADMIN_USERNAME == username)                                     # 입력한 username과 settings의 username같은지 판별.
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)             # pwd유효한지 판단.

        if login_valid and pwd_valid:                     # username, password 일치시에
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:                                                                                        # User가 없을 경우에 만들어준다.
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=username)                                                         # createsuperuser는 password반드시 넣어줘야 되서 안쓰는듯.
                user.is_staff = True                   # 이 계정은 password궂이 필요없는 계정.( 어짜피 위에서 입력시마다 authenticate로 검사하니까. <db 에서 가져오는것이 아님.> )
                user.is_superuser = True
                user.save()
            return user                                  # user 를 get했다면 여기서 반환. 없응면 except안에서 만들어서 반환.
        return None                                # pwd,username유효하지 않은경우는 아무것도 돌려주지 않는다.


    def get_user(self, user_id):                                  #이건 문서그대로 넣는다. (custom하기 전과 같은듯.)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class FacebookBackend:
    def authenticate(self,request, code):

        # 전달받은 인증코드를 사용해서 엑세스토큰을 받음.(facebook의 access_token주소로 get요청통해서)
        def get_access_token(code):
            # access token 얻기
            url = 'https://graph.facebook.com/v3.0/oauth/access_token'

            redirect_uri = 'https://maro5.com/members/facebook_login/'
            RUNSERVER = 'runserver' in sys.argv
            if RUNSERVER:
                redirect_uri = 'http://localhost:8000/members/facebook_login/'

            params = {
                'client_id': FACEBOOK_APP_ID,
                'redirect_uri': redirect_uri,
                'client_secret': FACEBOOK_APP_SECRET_CODE,
                'code': code,
            }

            response = requests.get(url, params)
            response_dict = response.json()
            access_token = response_dict.get('access_token',None)

            return access_token


        # face북의 debug_token주소 에 요청 보내고 결과 받기(받은 엑세스 토큰을 debug 결과에서 해당 토큰의 user_id(사용자 고유값) 가져올 수 있음.)
        # iput_token을 위의'access_token'
        # access_token은 {client_id}|{client_secret} 값.
        def get_debug_token(access_token):
            # aceess token 검사 --> fb id등 정보 받기

            url = 'https://graph.facebook.com/debug_token'

            params = {
                'input_token': access_token,
                'access_token': '{}|{}'.format(
                    FACEBOOK_APP_ID, FACEBOOK_APP_SECRET_CODE
                )
            }
            response = requests.get(url, params)

            # 위에서 받은 response중 이름등 추가적 가져오기 위해서 scope를 전달해 줘야 한다. ----> http에 추가해 놓았다.

            return response

        # GraphAPI의 ,'me'(User) 를 이용해서  Facebook User정보 받아오기.

        def get_user_info_by_GrapicAPI(access_token):  # , fields=None
            # 동적으로 params의 fields값을 채울 수 있도록 매개변수 및 함수 내 동작 변경.
            '''
            강사님 주석--->
            주어진 token에 해당하는 FacebooK User의 정보를 리턴.
            :param access_token:
            :return:fields: join()을 사용해 문자열을 만들 Sequence객체
            '''
            # GraphAPI를 통햬써 Facebook User정보 받아오기.
            url = 'https://graph.facebook.com/v3.0/me'

            params = {
                'fields':
                    ','.join(['id', 'name', 'first_name', 'last_name', 'picture']),
                'access_token': access_token,
            }
            response = requests.get(url, params)
            response_dict = response.json()

            return response_dict



        def create_user_from_facebook_user_info(response_dict):
            '''
            강사님주석
            Facebook GraphAPI의 'User'에 해당하는 응답인 user_info로부터
            id, first_name, last_name, picture항목을 사용해서
            Django의 User를 가져오거나 없는경우 새로 만듬(get_or_create)
            :param user_info_dict: Facebook GraphAPI -User응답.
            :return:
            '''

            # 받아온 정보 중 회원가입에 필요한 요소들 꺼내기
            facebook_user_id = response_dict['id']
            first_name = response_dict['first_name']
            last_name = response_dict['last_name']
            url_img_profile = response_dict['picture']['data']['url']


            return User.objects.get_or_create(
                username=facebook_user_id,  # 이값은 고유해서 get할때 사용 가능.
                defaults={  # 이값은 고유하지 않아도됨. 입력되는 값.
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

        access_token = get_access_token(code)

        if access_token:
            user_info_dict = get_user_info_by_GrapicAPI(
                access_token)  # ,fields=['id', 'name', 'first_name', 'last_name', 'picture']
            user, user_created = create_user_from_facebook_user_info(user_info_dict)
            return user

        return None

    def get_user(self,user_id):
        '''
        user_id(primary_key)값이 주어졌을때
        해당 User가 존재하면 반환하고 없으면 None을 반환한다.
        :param user_id: User모델의 primary_key값.
        :return: primary_key에 해당하는 USer가 존재하면 Userdl인스턴스 아니면 None
        '''

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class KakaotalkBackend:
    def authenticate(self, request, code):

        # 2 .access token 받기
        def get_access_token(code):
            url = "https://kauth.kakao.com/oauth/token"
            kakaotalk_redirect_uri = 'https://maro5.com/members/kakaotalk_login/'

            RUNSERVER = 'runserver' in sys.argv
            if RUNSERVER:
                kakaotalk_redirect_uri = 'http://localhost:8000/members/kakaotalk_login/'

            params = {
                'grant_type': 'authorization_code',
                'client_id': KAKAOTALK_REST_API_KEY,
                'redirect_uri': kakaotalk_redirect_uri,
                'code': code
            }

            response = requests.post(url, params)
            response_dict = response.json()
            access_token = response_dict.get('access_token',None)


            return access_token


        def get_user_info(access_token):  # , fields=None

            # 3. access token 이용해서 app loigin
            # 엡연결-로긴 은 로그인한 사용자와 앱을 카카오 플랫폼에 연결함으로서
            # 일반적인 사용자가 앱 가입/등록 요청을 하는 경우와 비슷하다.
            # 카카오 서비스 이용하기 위해서 로그인 후 앱연결 선행되야 하고 앱연결 올바로 수행되면 사용자대한 고유한 아이디 부여된다.
            url = "https://kapi.kakao.com/v1/user/signup"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cache-Control': 'no-cache',
            }
            headers.update({'Authorization': 'Bearer ' + str(access_token)})
            response = requests.post(url, headers=headers)
            # return HttpResponse(response)

            # 4. acces _token 이용해서 사용자 정보 요청.
            # 사용자의 id, 카카오 계정 email 및 상세정보 얻어올 수 있는 기능.
            # 사용자 로그인 후 얻은 사용자토큰, 엡연결이 되어있어야 한다.
            url = "https://kapi.kakao.com/v1/user/me"
            response = requests.post(url, headers=headers)
            # return HttpResponse(response)

            response_dict = response.json()

            return response_dict

        def create_user_from_kakaotalk_user_info(response_dict):
            id = response_dict['id']
            email = response_dict['kaccount_email']
            nickname = response_dict['properties']['nickname']
            url_img_profile = response_dict['properties']['profile_image']  # ['url']

            return User.objects.get_or_create(
                username=id,
                email=email,
            )

        access_token = get_access_token(code)

        if access_token:
            user_info_dict = get_user_info(
                access_token)  # ,fields=['id', 'name', 'first_name', 'last_name', 'picture']
            user, user_created = create_user_from_kakaotalk_user_info(user_info_dict)

            return user
        return None

    def get_user(self, user_id):

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


#
#
#
#
#
# class NaverBackend:
#     def authenticate(self, request, code):
#
#         def get_access_token(code):
#             return access_token
#
#         def get_debug_token(access_token):
#             return response
#
#
#         def get_user_info_by_GrapicAPI(access_token):  # , fields=None
#
#
#             return user_info_dict
#
#         def create_user_from_facebook_user_info(response_dict):
#
#
#             return User.objects.get_or_create(
#                 username=facebook_user_id,  # 이값은 고유해서 get할때 사용 가능.
#                 defaults={  # 이값은 고유하지 않아도됨. 입력되는 값.
#                     'first_name': first_name,
#                     'last_name': last_name,
#                 }
#             )
#
#         access_token = get_access_token(code)
#         user_info_dict = get_user_info_by_GrapicAPI(
#             access_token)  # ,fields=['id', 'name', 'first_name', 'last_name', 'picture']
#         user, user_created = create_user_from_facebook_user_info(user_info_dict)
#
#         return user
#
#     def get_user(self, user_id):
#
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
#
#
#
#
#
# class GoogleBackend:
#     def authenticate(self, request, code):
#
#         def get_access_token(code):
#             return access_token
#
#         def get_debug_token(access_token):
#             return response
#
#
#         def get_user_info_by_GrapicAPI(access_token):  # , fields=None
#
#
#             return user_info_dict
#
#         def create_user_from_facebook_user_info(response_dict):
#
#
#             return User.objects.get_or_create(
#                 username=facebook_user_id,  # 이값은 고유해서 get할때 사용 가능.
#                 defaults={  # 이값은 고유하지 않아도됨. 입력되는 값.
#                     'first_name': first_name,
#                     'last_name': last_name,
#                 }
#             )
#
#         access_token = get_access_token(code)
#         user_info_dict = get_user_info_by_GrapicAPI(
#             access_token)  # ,fields=['id', 'name', 'first_name', 'last_name', 'picture']
#         user, user_created = create_user_from_facebook_user_info(user_info_dict)
#
#         return user
#
#     def get_user(self, user_id):
#
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None