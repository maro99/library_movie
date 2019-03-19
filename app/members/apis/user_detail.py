import random
import string

from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import MovieLike
from members.serializers import UserInfoChangePageSerializer, ChangePasswordSerializer, ChangeEmailSerializer, \
    ChangePhoneNumberSerializer
from members.tokens import passwod_change_token

from members.tasks import send_info_change_email, send_sms

import traceback
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from movies.models import Movie
from movies.serializers import MovieMainSerializer

User = get_user_model()

class UserInfoChangePageView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        serializer = UserInfoChangePageSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # email로 인증번호 발송
    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(username=request.user)

            # password = serializer.validated_data['password']
            # password = urlsafe_base64_encode(force_bytes(password)).decode('utf-8')
            # uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')

            random_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
            change_password_token = passwod_change_token.make_token(user,random_number)
            send_info_change_email.delay(user.pk, random_number)

            # 추후 인증번호 검증시 필요한 token 같이 반환해줌.
            data = {
                'change_password_token': change_password_token,
                'detail': '인증번호가 발송되었습니다.',
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # 인증번호 검증 통해 비번 변경
    # 이때 token , 인증번호 body 에 같이 넣어줘야 한다.
    # token은 클라이언트(프론트) 에서 넣어주고  인증번호는 유저가 넣는다.
    def patch(self, request):

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():

            user = User.objects.get(username=request.user)
            random_number = request.data.get('random_number')
            change_password_token = request.data.get('change_password_token')
            password = serializer.validated_data['password']
            print(change_password_token )

            if passwod_change_token.check_token(user, change_password_token,random_number):
                user.set_password(password)
                user.save()
                data = {
                    'detail':'비밀번호가 변경되었습니다.'
                }
                return Response(data,status.HTTP_200_OK)
            else:
                data = {
                    'detail': '인증번호가 일치하지 않습니다.'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)



        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class UserChangeEmailView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # email로 인증번호 발송
    def post(self,request):
        serializer = ChangeEmailSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(username=request.user)

            changed_email = serializer.validated_data['email']
            random_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
            change_email_token = passwod_change_token.make_token(user,random_number)
            send_info_change_email.delay(user.pk, random_number,changed_email)

            # 추후 인증번호 검증시 필요한 token 같이 반환해줌.
            data = {
                'change_email_token': change_email_token,
                'detail': '인증번호가 발송되었습니다.',
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # 인증번호 검증 통해 비번 변경
    # 이때 token , 인증번호 body 에 같이 넣어줘야 한다.
    # token은 클라이언트(프론트) 에서 넣어주고  인증번호는 유저가 넣는다.
    def patch(self, request):

        serializer = ChangeEmailSerializer(data=request.data)

        if serializer.is_valid():

            user = User.objects.get(username=request.user)
            random_number = request.data.get('random_number')
            change_email_token = request.data.get('change_email_token')
            email = serializer.validated_data['email']

            if passwod_change_token.check_token(user, change_email_token,random_number):
                user.email = email
                user.save()
                data = {
                    'detail':'이메일이 변경되었습니다.'
                }
                return Response(data,status.HTTP_200_OK)
            else:
                data = {
                    'detail': '인증번호가 일치하지 않습니다.'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)



        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePhoneNumberView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # SMS 로 인증번호 발송
    def post(self,request):
        serializer = ChangePhoneNumberSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(username=request.user)

            changed_phone_number = serializer.validated_data['phone_number']
            random_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
            change_phone_number_token = passwod_change_token.make_token(user,random_number)
            send_sms.delay(user.pk, random_number,changed_phone_number)

            # 추후 인증번호 검증시 필요한 token 같이 반환해줌.
            data = {
                'change_phone_number_token': change_phone_number_token,
                'detail': '인증번호가 발송되었습니다.',
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # 인증번호 검증 통해 비번 변경
    # 이때 token , 인증번호 body 에 같이 넣어줘야 한다.
    # token은 클라이언트(프론트) 에서 넣어주고  인증번호는 유저가 넣는다.
    def patch(self, request):

        serializer = ChangePhoneNumberSerializer(data=request.data)

        if serializer.is_valid():

            user = User.objects.get(username=request.user)
            random_number = request.data.get('random_number')
            change_phone_number_token = request.data.get('change_phone_number_token')
            phone_number = serializer.validated_data['phone_number']

            if passwod_change_token.check_token(user, change_phone_number_token,random_number):
                user.phone_number = phone_number
                user.save()
                data = {
                    'detail':'휴대폰번호가 변경되었습니다.'
                }
                return Response(data,status.HTTP_200_OK)
            else:
                data = {
                    'detail': '인증번호가 일치하지 않습니다.'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)



        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMovieLikeList(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self,request):

        if request.user.is_authenticated:
            like_movies = request.user.like_movies
            serializer = MovieMainSerializer(like_movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        raise NotAuthenticated('로그인이 되어있지 않습니다.')


class UserMovieLike(APIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_movie_object(self,pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def post(self, request,pk,format=None):

        user = request.user
        movie = self.get_movie_object(pk=pk)

        if movie in user.like_movies:
            MovieLike.objects.filter(user=user,movie=movie).delete()
            data = {
                # 'detail': f'찜목록에서 {movie.title} 이 삭제 되었습니다. '
                'detail': f'찜목록에서 삭제 되었습니다. '

            }

        else:
            movielike = MovieLike(
                user=user,
                movie=movie,
            )
            movielike.save()

            data = {
                # 'detail': f'찜목록에 {movie.title} 이 추가되었습니다. '
                'detail': f'찜목록에 추가 되었습니다. '
            }

        return Response(data, status=status.HTTP_200_OK)


class UserSetAlarm(APIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request,type_num):

        user = request.user
        data = {}
        # 24시간 아후 타입에대한 요청일 경우
        if type_num == 24:
            if user.set_alarm_before_24h:
                user.set_alarm_before_24h = False
                data = {'detail': '영화 시작 24시간전 알람 해제됨'}
            else:
                user.set_alarm_before_24h = True
                data = {'detail': '영화 시작 24시간전 알람 설정됨'}

        # 3시간 이후 타입에 대한 요청이 경우
        elif type_num == 3:
            if user.set_alarm_before_3h:
                user.set_alarm_before_3h = False
                data = {'detail': '영화 시작 3시간전 알람 해제됨'}
            else:
                user.set_alarm_before_3h = True
                data = {'detail': '영화 시작 3시간전 알람 설정됨'}
        else:
            data = {'detail': '시간 타입 설정 오류 (24 or 3 시간중 하나로 설정 가능합니다.)'}



        user.save()

        return Response(data, status=status.HTTP_200_OK)



