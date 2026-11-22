from rest_framework import serializers
from django.core.validators import validate_integer
from django_jalali.serializers.serializerfield import JDateField

from .models import Profile
from .validators import validate_phone


class AuthenticatedSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[validate_integer, validate_phone])

class LoginOrRegisterSerializer(serializers.Serializer):
    code = serializers.CharField(required=False ,validators=[validate_integer])
    password = serializers.CharField(required=False)

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("user",)
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False},
            "password": {"required": False},
            "date_of_birth": {"required": False},
            "verified_email": {"required": False},
        }

class EditInformationSerializer(serializers.ModelSerializer):
    date_of_birth = JDateField()
    
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "date_of_birth")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "date_of_birth": {"required": True},
        }

class SetEmailUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if Profile.objects.filter(email = value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class EmailVerifySerializer(serializers.Serializer):
    code = serializers.CharField(validators=[validate_integer])

class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("The passwords do not match.")

        return attrs
    