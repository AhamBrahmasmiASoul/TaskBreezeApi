from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from rajneehsoulapiapp.login.models import AuthToken, MobileRegistration
from rajneehsoulapiapp.login.utils.utillity import parse_otp_timestamp, validate_mobile_no


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use Django's create_user method to ensure proper password hashing
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = ['key', 'user']
        extra_kwargs = {
            'key': {'required': True},
            'user': {'required': True},
        }


class MobileRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileRegistration
        fields = ['mobileNo']


class GetOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileRegistration
        fields = ['mobileNo', 'otp', 'fcmToken']

    def validate(self, data):
        mobile_no = data.get('mobileNo')
        otp = data.get('otp')

        # Refined mobile number validation logic
        validate_mobile_no(mobile_no)

        # Retrieve MobileRegistration or raise error if not found
        mobile_registration = get_object_or_404(MobileRegistration, mobileNo=mobile_no)

        # OTP validation
        if not otp or len(otp) != 4:
            raise serializers.ValidationError("OTP must be a 4-digit number.")

        # Use timezone.now() for current time comparison
        current_time = timezone.now()

        # Parse the OTP timestamp
        otp_time = parse_otp_timestamp(mobile_registration.otpTimeStamp)

        # Check OTP expiration (assuming otpTimeStamp is a datetime object)
        if (current_time - otp_time).total_seconds() > 120:
            raise serializers.ValidationError("OTP has expired.")

        if mobile_registration.otp != otp:
            raise serializers.ValidationError("Incorrect OTP.")

        return data
