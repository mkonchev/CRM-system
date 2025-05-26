from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.api.serializers.UserSerializer import UserSerializer
from apps.core.models.UserModel import User


@api_view(['GET'])
def user_list_view(request):
    user_list = User.objects.all()
    serializer = UserSerializer(user_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_by_id_view(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"detail": "Пользователь не найден"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def add_user_view(request):
    user = UserSerializer(data=request.data)

    # if user.objects.filter(**request.data).exists():
    #     raise serializers.ValidationError('This data already exists')

    if user.is_valid():
        user.save()
        return Response(data=user.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_user_view(request, pk):
    user = User.objects.get(pk=pk)
    upd_user = UserSerializer(instance=user, data=request.data, partial=True)

    if upd_user.is_valid():
        upd_user.save()
        return Response(data=upd_user.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_user_view(request, pk):
    if User.objects.filter(pk=pk).exists():
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        raise serializers.ValidationError('Not found this data')
