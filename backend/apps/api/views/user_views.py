from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.core.models.UserModel import User
from apps.api.serializers.UserSerializer import UserSerializer


class UserListView(generics.ListCreateAPIView):
    """
    GET /api/users/ - получить список всех пользователей
    POST /api/users/ - создать пользователя
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    GET /api/users/<id>/ - получить пользователя по ID
    PUT /api/users/<id>/ - полностью обновить пользователя
    PATCH /api/users/<id>/ - частично обновить пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_staff or obj.id == self.request.user.id:
            return obj
        from rest_framework.exceptions import PermissionDenied

        raise PermissionDenied("Нет доступа к этому пользователю")


class UserDeactivateView(APIView):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save()
        return Response({"message": "User deactivated"})
