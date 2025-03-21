import os

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from core import models
from core.utils import validate_max_length


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        error_messages={
            "required": "Please enter your firstname!",
            "blank": "Firstname cannot be empty!",
        },
    )
    last_name = serializers.CharField(
        required=True,
        error_messages={
            "required": "Please enter your lastname!",
            "blank": "Lastname cannot be empty!",
        },
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Please enter your email address!",
            "invalid": "Enter a valid email address!",
            "blank": "Email cannot be empty!",
        },
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            "required": "Please enter your password!",
            "blank": "Password cannot be empty!",
        },
    )
    role = serializers.IntegerField(default=1)

    class Meta:
        model = models.User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "avatar",
            "full_name",
            "status",
        ]
        extra_kwargs = {"password": {"write_only": True}}

        def get_full_name(self, obj):
            return obj.full_name

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get("avatar"):
            representation["avatar"] = (
                f"{os.environ.get("BE_DOMAIN")}{representation['avatar']}"
            )
        return representation


class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        error_messages={
            "required": "Please enter your firstname!",
            "blank": "Firstname cannot be empty!",
        },
    )
    last_name = serializers.CharField(
        required=True,
        error_messages={
            "required": "Please enter your lastname!",
            "blank": "Lastname cannot be empty!",
        },
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Please enter your email address!",
            "invalid": "Enter a valid email address!",
            "blank": "Email cannot be empty!",
        },
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            "required": "Please enter your password!",
            "blank": "Password cannot be empty!",
        },
    )
    role = serializers.IntegerField(default=1)

    class Meta:
        model = models.User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "avatar",
            "full_name",
            "status",
        ]
        extra_kwargs = {"password": {"write_only": True}}

        def get_full_name(self, obj):
            return obj.full_name

    def validate(self, data):
        char_fields = ["first_name", "last_name", "password"]
        for field in char_fields:
            if field in data:
                validate_max_length(
                    data[field],
                    self.Meta.model._meta.get_field(field).max_length,
                    field.capitalize(),
                )
        return data

    def validate_email(self, value):
        if models.User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Email already exists!")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            if len(exc.messages) > 1:
                raise serializers.ValidationError(
                    "Your password must contain at least 8 characters, one uppercase letter, one digit, and one special character!"
                )
            else:
                raise serializers.ValidationError(exc.messages)
        return value

    def create(self, validated_data):
        validated_data["email"] = validated_data["email"].lower()
        user = models.User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Please enter email address!",
            "invalid": "Enter a valid email address!",
            "blank": "Email cannot be empty!",
        },
    )
    password = serializers.CharField(
        required=True,
        error_messages={
            "required": "Please enter your password!",
            "blank": "Password cannot be empty!",
        },
    )

    class Meta:
        model = models.User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    token_class = RefreshToken

    def validate(self, attrs):
        try:
            refresh = self.token_class(attrs["refresh_token"])
        except TokenError as e:
            raise InvalidToken(f"{str(e)}!")
        except InvalidToken as e:
            raise InvalidToken(f"{str(e)}!")

        if not refresh:
            raise AuthenticationFailed("No refresh token provided.")

        data = {"access_token": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh_token"] = str(refresh)

        return data


class UserSerializerWithToken(UserSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["refresh_token"] = self.context.get("refresh_token")
        representation["access_token"] = self.context.get("access_token")
        return representation
