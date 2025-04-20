from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.api.serializers.CarSerializer import CarSerializer
from apps.car.models.CarModel import Car


@api_view(['GET'])
def car_list_view(request):
    car_list = Car.objects.all()
    serializer = CarSerializer(car_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def car_by_id(request, pk):
    car = Car.objects.get(pk=pk)
    serializer = CarSerializer(car)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
