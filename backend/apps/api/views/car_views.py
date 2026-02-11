from rest_framework import generics, permissions
from apps.car.models.CarModel import Car
from apps.api.serializers.CarSerializer import CarSerializer


class CarListView(generics.ListCreateAPIView):
    """
    GET /api/cars/ - получить список всех машин
    POST /api/cars/ - создать новую машину
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    permission_classes = [permissions.AllowAny]


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/cars/<id>/ - получить машину по ID
    PUT /api/cars/<id>/ - полностью обновить машину
    PATCH /api/cars/<id>/ - частично обновить машину
    DELETE /api/cars/<id>/ - удалить машину
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    permission_classes = [permissions.AllowAny]
