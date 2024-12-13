from rest_framework import serializers
from .models import *
from django.core.cache import cache

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    role = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=4, required=False)

    class Meta:
        model    = CustomUser
        fields   = ['id', 'email', 'password', 'role', 'full_name', 'is_active']

    def validate_email(self, value):
        """Check if the email is already in use."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_role(self, value):
        """Check if the role is valid."""
        valid_roles = [choice[0] for choice in CustomUser.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(f"{value} is not a valid role.")
        return value
    

class OTPSerializer(serializers.Serializer):
    email    = serializers.EmailField(required=True)
    otp      = serializers.CharField(required=True, min_length=6, max_length=6)
    password = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        # Validate that the OTP matches the one stored in the cache.
        cached_otp = cache.get(f"otp_{email}")
        print('cached_otp:', cached_otp)
        if cached_otp is None:
            raise serializers.ValidationError({"otp": "OTP has expired."})
        if cached_otp != otp:
            raise serializers.ValidationError({"otp": "Invalid OTP."})

        return data
   