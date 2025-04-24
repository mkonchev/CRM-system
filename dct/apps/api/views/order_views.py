from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.api.serializers.OrderSerializer import OrderSerializer
from apps.order.models.OrderModel import Order


@api_view(['GET'])
def order_list_view(request):
    order_list = Order.objects.all()
    serializer = OrderSerializer(order_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def order_by_id_view(request, pk):
    order = Order.objects.get(pk=pk)
    serializer = Order(order)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_order_view(request):
    order = OrderSerializer(data=request.data)

    # if Order.objects.filter(**request.data).exists():
    #     raise serializers.ValidationError('This data already exists')

    if order.is_valid():
        order.save()
        return Response(data=order.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_order_view(request, pk):
    order = Order.objects.get(pk=pk)
    upd_order = OrderSerializer(instance=order, data=request.data)

    # if Order.objects.filter(**request.data).exists():
    #     raise serializers.ValidationError('This data already exists')

    if upd_order.is_valid():
        upd_order.save()
        return Response(data=upd_order.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_order_view(request, pk):
    if Order.objects.filter(pk=pk).exists():
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        raise serializers.ValidationError('Not found this data')
