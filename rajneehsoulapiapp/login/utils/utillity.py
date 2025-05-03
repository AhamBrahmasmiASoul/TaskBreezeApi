import binascii
import os
import random
from datetime import datetime, timedelta

import pytz
from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token

from rajneehsoulapiapp.app_utility.utils import create_response, custom_error_response
from rajneehsoulapiapp.login.const import otp_validity_period
from rajneehsoulapiapp.login.models import AuthToken, EmailIdRegistration


def generate_otp() -> int:
    """Generate a 6-digit random OTP."""
    return random.randint(1000, 9999)


def get_current_time() -> datetime:
    """Get the current local time in Asia/Kolkata timezone."""
    return datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(minutes= otp_validity_period)


def handle_existing_token(auth_token_object, mobile_reg_data):
    """Check token expiration and update or reuse accordingly."""
    if auth_token_object.is_expired():
        # Generate new key since the old one is expired
        new_key = binascii.hexlify(os.urandom(20)).decode()
        auth_token_object.key = new_key
        auth_token_object.refresh_expiry()
    else:
        # Extend token validity without changing the key
        auth_token_object.refresh_expiry()

    auth_token_object.save()

    from rajneehsoulapiapp.login.serializers import CustomAuthTokenSerializer
    serializer = CustomAuthTokenSerializer(auth_token_object)

    return create_response(data={
        "authData": serializer.data,
        "emailId": mobile_reg_data.emailId
    }, status_code=status.HTTP_200_OK)


def handle_new_token(mobile_reg_data, custom_user):
    """Create a new token with an expiry time of 2 minutes."""
    new_key = binascii.hexlify(os.urandom(20)).decode()
    auth_token_object = AuthToken.objects.create(
        key=new_key,
        user_id=mobile_reg_data.id,
        expires_at=datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(hours=12)  # Set expiry time ? TO DO
    )

    custom_user.auth_token = auth_token_object  # Assuming a field exists
    custom_user.save()

    from rajneehsoulapiapp.login.serializers import CustomAuthTokenSerializer
    serializer = CustomAuthTokenSerializer(auth_token_object)

    return create_response(data={
        "authData": serializer.data,
        "emailId": mobile_reg_data.emailId
    }, status_code=status.HTTP_200_OK)

def update_or_create_email_id_registration(email_id: str, otp: str, timestamp: str) -> None:
    """Helper method to update or create a mobile registration."""
    EmailIdRegistration.objects.update_or_create(
        emailId=email_id,
        defaults={"otp": otp, "otpTimeStamp": timestamp},
    )


def parse_otp_timestamp(otp_timestamp):
    """
    Helper function to parse OTP timestamp from string to timezone-aware datetime.
    """
    try:
        otp_time = datetime.strptime(otp_timestamp.split('.')[0], '%Y-%m-%d %H:%M:%S')
        return timezone.make_aware(otp_time, timezone.get_current_timezone())
    except ValueError:
        raise serializers.ValidationError("Invalid OTP timestamp format.")
