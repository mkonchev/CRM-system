from rest_framework import serializers

# from apps.api.serializers.CarSerializer import CarSerializer
# from apps.api.serializers.OrderSerializer import OrderSerializer
from apps.workstatus.models.WorkstatusModel import Workstatus


class WorkstatusSerializer(serializers.ModelSerializer):

    # car = CarSerializer()
    # order = OrderSerializer()

    class Meta:
        model = Workstatus
        fields = '__all__'
