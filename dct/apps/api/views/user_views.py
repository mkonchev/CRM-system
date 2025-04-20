from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.api.serializers.UserSerializer import UserSerializer
from apps.core.models.UserModel import User


@api_view(['GET'])
def user_list_view(request):
    user_list = User.objects.all()
    serializer = UserSerializer(user_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
