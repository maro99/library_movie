from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


User = get_user_model()


class SignoutView(APIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        request.user.auth_token.delete()
        request.user.delete()
        data = {
            "detail": "회원탈퇴 되었습니다."
        }

        return Response(data, status=status.HTTP_200_OK)