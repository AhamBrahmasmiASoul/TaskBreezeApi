import pytz
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from rajneehsoulapiapp.login.const import validity_period, otp_length
from rajneehsoulapiapp.login.models import AuthToken, EmailIdRegistration, IST
from rajneehsoulapiapp.login.utils.utillity import parse_otp_timestamp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use Django's create_user method to ensure proper password hashing
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.ModelSerializer):
    expires_at = serializers.SerializerMethodField()  # Convert to IST before returning

    class Meta:
        model = AuthToken
        fields = ['key', 'user', 'expires_at']

    def get_expires_at(self, obj):  # Ensure this method is inside the class
        """Convert expires_at to IST before returning."""
        return obj.expires_at.astimezone(IST).strftime('%Y-%m-%d %H:%M:%S')


class MobileRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailIdRegistration
        fields = ['emailId']


class GetOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailIdRegistration
        fields = ['emailId', 'otp', 'fcmToken']

    def validate(self, data):
        email_id = data.get('emailId')
        otp = data.get('otp')


        # Retrieve MobileRegistration or raise error if not found
        email_id_registration = get_object_or_404(EmailIdRegistration, emailId=email_id)

        # OTP validation
        if not otp or len(otp) != otp_length:
            raise serializers.ValidationError(f"OTP must be a {otp_length}-digit number.")

        # Use timezone.now() for current time comparison
        current_time = timezone.now()

        # Parse the OTP timestamp
        otp_time = parse_otp_timestamp(email_id_registration.otpTimeStamp)

        # Check OTP expiration (assuming otpTimeStamp is a datetime object)
        if (current_time - otp_time).total_seconds() > validity_period:
            raise serializers.ValidationError("OTP has expired.")

        if email_id_registration.otp != otp:
            raise serializers.ValidationError("Incorrect OTP.")

        return data
