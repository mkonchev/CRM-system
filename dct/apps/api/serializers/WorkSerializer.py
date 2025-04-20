from rest_framework import serializers

# from apps.api.serializers.CarSerializer import CarSerializer
from apps.work.models.WorkModel import Work


class WorkSerializer(serializers.ModelSerializer):

    # car = CarSerializer()

    class Meta:
        model = Work
        fields = '__all__'
