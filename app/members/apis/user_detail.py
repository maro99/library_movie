from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import UserDetailSerializer


class UserDetailView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)