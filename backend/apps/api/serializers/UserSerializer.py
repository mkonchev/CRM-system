from rest_framework import serializers
from apps.core.models.UserModel import User


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'phone_number', 'tg_login', 'email', 'role'
        ]

        read_only_fields = ['id']
