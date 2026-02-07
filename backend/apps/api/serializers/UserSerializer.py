from rest_framework import serializers

from apps.core.models.UserModel import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
