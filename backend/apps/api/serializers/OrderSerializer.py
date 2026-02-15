from rest_framework import serializers
from apps.order.models.OrderModel import Order


class OrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""

    class Meta:
        model = Order
        fields = [
            'id',
            'owner',
            'car',
            'worker',
            'start_date',
            'end_date',
            'is_completed'
        ]

        read_only_fields = ['id', 'start_date']
