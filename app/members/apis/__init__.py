import traceback

from django.contrib.auth import authenticate, login, get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from members.serializers import UserSerializer
from members.tokens import account_activation_token

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AuthToken(APIView):
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

class Signup(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        # raise serializer.validationError
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivate(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
            user = User.objects.get(pk=uid)

        except(TypeError. ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(user.email+ '계정이 활성화 되었습니다.', status=status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다.', status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(traceback.format_exc())










