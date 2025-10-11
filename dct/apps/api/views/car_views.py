from rest_framework import status, serializers, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers.CarSerializer import CarSerializer
from apps.car.models.CarModel import Car


class CarListView(APIView):
    name = 'car-list-view'
    serializer_class = CarSerializer

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all cars.
        """
        queryset = Car.objects.all()
        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @api_view(['GET'])
    # def car_list_view(request):
    #     car_list = Car.objects.all()
    #     serializer = CarSerializer(car_list, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)


class CarView(APIView):
    name = 'car-view'
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk, format=None):
        """
        Return car by id.
        """
        queryset = Car.objects.filter(pk=pk)
        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def car_by_id_view(request, pk):
#     if Car.objects.filter(pk=pk).exists():
#         car = Car.objects.get(pk=pk)
#         serializer = CarSerializer(car)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#     else:
#         raise serializers.ValidationError('Not found this data')


class CarAddView(APIView):
    name = 'car-add-view'
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def add(self, request, pk, format=None):
        """
        Add new car.
        """
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


# class CarDeleteView(APIView):
#     name = 'car-view'
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer

#     # authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request, pk, format=None):


# @api_view(['DELETE'])
# def delete_car_view(request, pk):
#     if Car.objects.filter(pk=pk).exists():
#         car = Car.objects.get(pk=pk)
#         car.delete()
#         return Response(status=status.HTTP_202_ACCEPTED)
#     else:
#         raise serializers.ValidationError('Not found this data')
