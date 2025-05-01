from rest_framework import serializers

# from apps.work.models.WorkModel import Work
from apps.order.models.OrderModel import Order


class OrderSerializer(serializers.ModelSerializer):

    # works = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Work.objects.all())
    # workstatus = serializers.PrimaryKeyRelatedField(
    #     many=True, read_only=True, source='order_works')

    class Meta:
        model = Order
        fields = '__all__'
