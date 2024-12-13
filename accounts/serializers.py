from rest_framework import serializers
from django.contrib.auth import authenticate
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
    

class SignupOTPSerializer(serializers.Serializer):
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
   

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validates the email and password combination.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("No user is associated with this email.")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        if not user.is_active:
            raise serializers.ValidationError("You are blocked by admin. Please contact the admin.")

        attrs['user'] = user
        return attrs
    
class LoginOTPSerializer(serializers.Serializer):
    email    = serializers.EmailField(required=True)
    otp      = serializers.CharField(required=True, min_length=6, max_length=6)
    password = serializers.CharField(required=True)

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