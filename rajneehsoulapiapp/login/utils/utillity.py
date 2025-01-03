import binascii
import os
import random
from datetime import datetime

import pytz
from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token

from rajneehsoulapiapp.app_utility.utils import create_response, custom_error_response
from rajneehsoulapiapp.login.models import AuthToken, MobileRegistration


def generate_otp() -> int:
    """Generate a 4-digit random OTP."""
    return random.randint(1000, 9999)


def get_current_time() -> datetime:
    """Get the current local time in Asia/Kolkata timezone."""
    return datetime.now(pytz.timezone('Asia/Kolkata'))


def handle_existing_token(auth_token_object, mobile_reg_data):
    # Generate new token and update AuthToken
    new_key = binascii.hexlify(os.urandom(20)).decode()
    from rajneehsoulapiapp.login.serializers import CustomAuthTokenSerializer
    serializer = CustomAuthTokenSerializer(auth_token_object, data={"key": new_key, "user": mobile_reg_data.id},
                                           partial=True)

    if serializer.is_valid():
        serializer.save()
        return create_response(data={
            "authData": serializer.data,
            "mobileNo": mobile_reg_data.mobileNo
        }, status_code=status.HTTP_200_OK)

    return custom_error_response(serializer)


def handle_new_token(mobile_reg_data, custom_user):
    # Create a new AuthToken and save
    new_key = binascii.hexlify(os.urandom(20)).decode()
    auth_token_object = AuthToken.objects.create(
        key=new_key,
        user_id=mobile_reg_data.id
    )
    # Associate the new AuthToken with the CustomUser
    custom_user.auth_token = auth_token_object  # Assuming you have a `auth_token` field in the CustomUser model
    custom_user.save()

    from rajneehsoulapiapp.login.serializers import CustomAuthTokenSerializer
    serializer = CustomAuthTokenSerializer(auth_token_object)
    return create_response(data={
        "authData": serializer.data,
        "mobileNo": mobile_reg_data.mobileNo
    }, status_code=status.HTTP_200_OK)


def update_or_create_mobile_registration(mobile_no: str, otp: str, timestamp: str) -> None:
    """Helper method to update or create a mobile registration."""
    MobileRegistration.objects.update_or_create(
        mobileNo=mobile_no,
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


def validate_mobile_no(value):
    if not value.startswith("+91") or len(value) != 13:
        raise serializers.ValidationError(
            "Invalid mobile number format. It must start with +91 and be 13 characters long.")
    return value
