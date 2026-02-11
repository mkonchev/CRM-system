from rest_framework import serializers
from apps.core.models.UserModel import User


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm', None)
        return User.objects.create_user(
            **validated_data,
            password=password
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'phone_number', 'tg_login', 'email', 'role',
            'password', 'password_confirm'
        ]

        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }
