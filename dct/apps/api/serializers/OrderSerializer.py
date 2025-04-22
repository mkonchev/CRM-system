from rest_framework import serializers

# from apps.api.serializers.WorkSerializer import WorkSerializer
from apps.order.models.OrderModel import Order


class OrderSerializer(serializers.ModelSerializer):

    # works = WorkSerializer(many=True)
    # workstatus = serializers.PrimaryKeyRelatedField(
    #     many=True, read_only=True, source='order_works')

    class Meta:
        model = Order
        fields = '__all__'
