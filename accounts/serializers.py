from rest_framework import serializers
from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password.")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationFailed("Your account has been blocked by the admin.")

        self.user = user
        return super().validate(attrs)





class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


User = get_user_model()


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False, min_length=6
    )

    class Meta:
        model = User
        fields = ["id", "name", "password","is_staff"]

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        # Update normal fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle password properly
        if password:
            instance.set_password(password)

        instance.save()
        return instance



from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("access_token")

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                audience=None  # We will validate manually
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise serializers.ValidationError("Wrong issuer.")

        except Exception:
            raise serializers.ValidationError("Invalid or expired Google token.")

        email = idinfo.get("email")
        name = idinfo.get("name")

        if not email:
            raise serializers.ValidationError("Email not provided by Google.")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"name": name}
        )

        if created:
            user.set_unusable_password()
            user.save()

        tokens = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(tokens.access_token),
            "refresh": str(tokens),
        }
