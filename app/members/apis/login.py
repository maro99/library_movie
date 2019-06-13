import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from django.contrib.auth import authenticate, login, get_user_model
from members.serializers import UserSerializer, AccessTokenSerializer

User = get_user_model()

class Login(APIView):
    def post(self,request):
        # 전달받은 데이터에서 usernmae, passqord 추출
        username = request.data.get('username')
        password = request.data.get('password')

        # authenticate
        user = authenticate(username=username, password=password)

        if user:
            # Token을 가져오거나 생성
            token,__ = Token.objects.get_or_create(user=user)
            # Response에 돌려줄 데이터
            data = {
                "token":token.key,
            }
            return Response(data)

        # authenticate에 실패한 경우
        raise AuthenticationFailed( '인증정보가 올바르지 않습니다.')



class AuthenticationTest(APIView):
    # URL:/api/users/auth-test/
    def get(self,request):
        # reqeust.user가 인증 된 상태일 경우, UserSerializer를 사용해 렌더링한 데이터를 보내줌.
        # 인증되지 않았을 영우 NotAuthenticated Exception raise
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        raise NotAuthenticated('로그인이 되어있지 않습니다.')



class GoogleAuthToken(APIView):
    def post(self, request):
        #  URL: /api/users/facebook-login/
        # request.data에 'facebook_id'와 'first_name', 'last_name'이 올 것으로 예상
        # 1. 전달받은 facebook_id에 해당하는 유저가 존재하면 해당 User에
        # 2. 생성한 User에
        #   -> 해당하는 Token을 가져오거나 새로 생성해서 리턴
        # 결과는 Postman으로 확인

        access_token = request.data.get('access_token')
        def get_user_info(access_token):

        # 3. access token 이용해서 회원프로필 조회
            url = "https://www.googleapis.com/oauth2/v1/userinfo"

            params = {
                 'access_token': access_token, 'alt': 'json'
            }

            response = requests.get(url, params=params)
            print(f'response: {response}')
            #
            # return HttpResponse(response)
            # {"id": "108743605198166301707", "name": "Sanmaro Na", "given_name": "Sanmaro", "family_name": "Na",
            #  "link": "https://plus.google.com/108743605198166301707",
            #  "picture": "https://lh6.googleusercontent.com/-cYOpZZldajQ/AAAAAAAAAAI/AAAAAAAABtw/q8-Hofd6_QY/photo.jpg",
            #  "gender": "male", "locale": "ko"}

            response_dict = response.json()

            return response_dict

        def create_user_from_google_user_info(response_dict):
            id = response_dict.get('id')
            given_name = response_dict.get('given_name')
            family_name = response_dict.get('family_name')
            email = response_dict.get('email')

            if given_name and family_name and email:
                defaults={
                    'first_name': given_name,  # 이값은 고유해서 get할때 사용 가능.
                    'last_name': family_name,  # 이값은 고유하지 않아도됨. 입력되는 값.
                    'email': email,
                }
            elif given_name and email:
                defaults={
                    'first_name': given_name,
                    'email': email,
                }
            elif family_name and email:
                defaults={
                    'last_name': family_name,
                    'email': email,
                }

            return User.objects.get_or_create(

                username=id,
                defaults=defaults
            )

        user_info_dict = get_user_info(access_token)  # ,fields=['id', 'name', 'first_name', 'last_name', 'picture']

        print(f"user_info_dict: {user_info_dict}")
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@222')

        if user_info_dict:
            user, user_created = create_user_from_google_user_info(user_info_dict)

            if user:
                token, __ = Token.objects.get_or_create(user=user)
                # Response에 돌려줄 데이터
                data = {
                    "token": token.key,
                }
                return Response(data)

        raise AuthenticationFailed('인증정보가 올바르지 않습니다.')
