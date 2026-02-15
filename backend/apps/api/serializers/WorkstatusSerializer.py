from rest_framework import serializers
from apps.workstatus.models.WorkstatusModel import Workstatus


class WorkstatusSerializer(serializers.ModelSerializer):
    """Workstatus Serializer"""

    class Meta:
        model = Workstatus
        fields = [
            'id',
            'work',
            'order',
            'status',
            'amount',
            'fix_price'
        ]

        read_only_fields = ['id']
