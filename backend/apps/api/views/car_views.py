from rest_framework import generics, permissions
from apps.car.models.CarModel import Car
from apps.api.serializers.CarSerializer import CarSerializer
from apps.core.models.consts import UserRoleChoice


class CarListView(generics.ListCreateAPIView):
    """
    GET /api/cars/ - получить список всех машин
    POST /api/cars/ - создать новую машину
    """

    serializer_class = CarSerializer

    def get_permissions(self):
        """Права доступа для разных методов"""
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Фильтрация машин по владельцу"""
        user = self.request.user

        if not user.is_authenticated:
            return Car.objects.none()

        if user.is_staff or user.role == UserRoleChoice.worker:
            return Car.objects.all().order_by("id")

        return Car.objects.filter(owner=user).order_by("id")

    def perform_create(self, serializer):
        """Назначаем владельца"""
        user = self.request.user

        if not self.request.data.get("vin"):
            from rest_framework.exceptions import ValidationError

            raise ValidationError({"vin": "VIN обязателен для заполнения"})

        if user.is_staff or user.role == UserRoleChoice.worker:
            owner_id = self.request.data.get("owner")
            if owner_id:
                serializer.save(owner_id=owner_id)
                return
        serializer.save(owner=user)


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/cars/<id>/ - получить машину по ID
    PUT /api/cars/<id>/ - полностью обновить машину
    PATCH /api/cars/<id>/ - частично обновить машину
    DELETE /api/cars/<id>/ - удалить машину
    """

    serializer_class = CarSerializer

    def get_permissions(self):
        """Права доступа для детального просмотра"""
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """Проверка доступа к конкретной машине"""
        user = self.request.user

        if not user.is_authenticated:
            return Car.objects.none()

        if (
            user.is_staff
            or user.role == UserRoleChoice.worker
            or user.role == UserRoleChoice.admin
        ):  # noqa
            return Car.objects.all()

        return Car.objects.filter(owner=user)
