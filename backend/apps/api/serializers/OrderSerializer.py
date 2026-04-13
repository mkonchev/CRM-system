from rest_framework import serializers
from apps.order.models.OrderModel import Order
from apps.api.serializers.WorkstatusSerializer import WorkstatusSerializer
from apps.api.serializers.CarSerializer import CarSerializer
from apps.api.serializers.UserSerializer import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""
    items = WorkstatusSerializer(source='items.all', many=True, read_only=True)

    owner_details = UserSerializer(source='owner', read_only=True)
    worker_details = UserSerializer(source='worker', read_only=True)
    car_details = CarSerializer(source='car', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'owner',
            'owner_details',
            'car',
            'car_details',
            'worker',
            'worker_details',
            'start_date',
            'end_date',
            'is_completed',
            'items'
        ]

        read_only_fields = ['id', 'start_date']
