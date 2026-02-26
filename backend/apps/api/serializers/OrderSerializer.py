from rest_framework import serializers
from apps.order.models.OrderModel import Order
from apps.api.serializers.WorkstatusSerializer import WorkstatusSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""
    items = WorkstatusSerializer(source='items.all', many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'owner',
            'car',
            'worker',
            'start_date',
            'end_date',
            'is_completed',
            'items'
        ]

        read_only_fields = ['id', 'start_date']
