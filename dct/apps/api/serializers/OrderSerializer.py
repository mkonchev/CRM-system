from rest_framework import serializers

# from apps.api.serializers.CarSerializer import CarSerializer
# from apps.api.serializers.UserSerializer import UserSerializer
from apps.api.serializers.WorkSerializer import WorkSerializer
from apps.order.models.OrderModel import Order


class OrderSerializer(serializers.ModelSerializer):

    # owner = UserSerializer()
    # car = CarSerializer()
    works = WorkSerializer(many=True)
    # worker = UserSerializer()
    workstatus = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='order_work_status')

    class Meta:
        model = Order
        fields = '__all__'
