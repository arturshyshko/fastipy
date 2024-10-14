from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        try:
            validate_password(value)  # Running Django password validators.
        except ValidationError as e:
            raise serializers.ValidationError from e

        return value


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class UserAuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
