from rest_framework import serializers
from apps.car.models.CarModel import Car


class CarSerializer(serializers.ModelSerializer):
    """Car Serializer"""

    class Meta:
        model = Car
        fields = ["id", "number", "mark", "model", "vin", "year", "owner"]
        read_only_fields = ["id"]

        def validate_vin(self, value):
            """Проверка VIN"""
            if not value:
                raise serializers.ValidationError("Поле VIN обязательно")
            return value
