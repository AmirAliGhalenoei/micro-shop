from rest_framework import serializers
from django.core.validators import validate_integer

from .validators import validate_phone



class AuthenticatedSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_integer, validate_phone])

class LoginOrRegisterSerializer(serializers.Serializer):
    code = serializers.CharField(required=False ,validators=[validate_integer])
    password = serializers.CharField(required=False)

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()