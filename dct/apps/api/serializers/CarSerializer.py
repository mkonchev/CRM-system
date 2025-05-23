from rest_framework import serializers

from apps.car.models.CarModel import Car


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'
