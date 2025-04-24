from rest_framework import status, serializers
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
def car_by_id_view(request, pk):
    if Car.objects.filter(pk=pk).exists():
        car = Car.objects.get(pk=pk)
        serializer = CarSerializer(car)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        raise serializers.ValidationError('Not found this data')


@api_view(['POST'])
def add_car_view(request):
    car = CarSerializer(data=request.data)

    if Car.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if car.is_valid():
        car.save()
        return Response(data=car.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_car_view(request, pk):
    car = Car.objects.get(pk=pk)
    upd_car = CarSerializer(instance=car, data=request.data)

    if upd_car.is_valid():
        upd_car.save()
        return Response(data=upd_car.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_car_view(request, pk):
    if Car.objects.filter(pk=pk).exists():
        car = Car.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        raise serializers.ValidationError('Not found this data')
