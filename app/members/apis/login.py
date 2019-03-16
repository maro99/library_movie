from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from django.contrib.auth import authenticate, login, get_user_model
from members.serializers import UserSerializer



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

        google_id = request.data.get('google_id')
        # last_name = request.data.get('last_name')
        # first_name = request.data.get('first_name')

        user, __ = User.objects.get_or_create(
            username=google_id,

        )
        # 해당 User와 연결되는 Token생성
        token, __ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)
