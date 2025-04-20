from rest_framework import serializers

from apps.api.serializers.UserSerializer import UserSerializer
from apps.car.models.CarModel import Car


class CarSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Car
        fields = '__all__'
