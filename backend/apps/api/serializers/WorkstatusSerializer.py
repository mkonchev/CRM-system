from rest_framework import serializers
from apps.workstatus.models.WorkstatusModel import Workstatus


class WorkstatusSerializer(serializers.ModelSerializer):
    """Workstatus Serializer"""
    fix_price = serializers.IntegerField(required=False)

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

    def create(self, validated_data):
        print("🔥🔥🔥 CREATE ВЫЗВАН!")
        print("📦 validated_data:", validated_data)
        # Если fix_price не передан — берём из работы
        if 'fix_price' not in validated_data:
            work = validated_data['work']
            validated_data['fix_price'] = work.price
        return super().create(validated_data)
