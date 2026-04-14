from rest_framework import generics, permissions
from apps.car.models.CarModel import Car
from apps.api.serializers.CarSerializer import CarSerializer
from apps.core.models.consts import UserRoleChoice


class CarListView(generics.ListCreateAPIView):
    """
    GET /api/cars/ - получить список всех машин
    POST /api/cars/ - создать новую машину
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        """Права доступа для разных методов"""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Фильтрация машин по владельцу"""
        queryset = Car.objects.all()
        if self.request.user.is_authenticated:
            if self.request.user.is_staff or self.request.user.role == UserRoleChoice.worker: # noqa
                return queryset
            return queryset.filter(owner=self.request.user)
        return Car.objects.none()

    def perform_create(self, serializer):
        """Автоматически назначаем владельцем текущего пользователя,
          если роль-User"""
        user = self.request.user
        if user.is_staff or user.role == UserRoleChoice.worker:
            owner_id = self.request.data.get('owner')
            if owner_id:
                serializer.save(owner_id=owner_id)
        serializer.save(owner=user)


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/cars/<id>/ - получить машину по ID
    PUT /api/cars/<id>/ - полностью обновить машину
    PATCH /api/cars/<id>/ - частично обновить машину
    DELETE /api/cars/<id>/ - удалить машину
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        """Права доступа для детального просмотра"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Проверка доступа к конкретной машине"""
        if self.request.user.is_authenticated:
            if self.request.user.is_staff or self.request.user.role == UserRoleChoice.worker: # noqa
                return Car.objects.all()
            return Car.objects.filter(owner=self.request.user)
        return Car.objects.none()
