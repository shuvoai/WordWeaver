import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk', 'username', 'first_name', 'last_name', 'email', 'date_joined',
            'is_active', 'is_staff', 'is_superuser',
        ]

    def validate_password(self, data):
        validators.validate_password(password=data)
        return data


class UserSerializer(BaseUserSerializer):
    pass


class UserCreateSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email'
        ]
        read_only_fields = ['username']
