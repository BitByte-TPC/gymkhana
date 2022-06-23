from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.auth.models import Token


class CreateTokenRequestSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class TokenUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'is_active']


class CreateTokenResponseSerializer(serializers.ModelSerializer):
    user = TokenUserSerializer(read_only=True)

    class Meta:
        model = Token
        fields = ['token', 'user']
