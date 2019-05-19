import traceback

from django.contrib.auth import  get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import UserSerializer
from members.tokens import account_activation_token

User = get_user_model()


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


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
            # uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
            uid = force_text(urlsafe_base64_decode(uidb64))
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




class SignupServerTest(APIView):

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()

            return Response('서버측 유효성 검사 성공', status=status.HTTP_200_OK)

        # raise serializer.validationError
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





