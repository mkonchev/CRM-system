from rest_framework import serializers
from apps.work.models.WorkModel import Work


class WorkSerializer(serializers.ModelSerializer):
    """Work Serializer"""

    class Meta:
        model = Work
        fields = ['id', 'name', 'description', 'car', 'price']

        read_only_fields = ['id']
