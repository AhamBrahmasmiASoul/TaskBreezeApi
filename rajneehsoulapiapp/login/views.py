from django.shortcuts import get_object_or_404
from requests import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rajneehsoulapiapp.login.models import MobileRegistration, AuthToken, CustomUser
from rajneehsoulapiapp.login.utils.utillity import (
    handle_existing_token,
    handle_new_token,
    custom_error_response,
    create_response, update_or_create_mobile_registration, generate_otp, get_current_time,
)


@api_view(["POST"])
def get_otp_api(request: Request) -> Response:
    """Handle mobile login requests."""
    received_mobile_no = request.data.get("mobileNo")
    if not received_mobile_no:
        return custom_error_response("Mobile number is required.")

    from rajneehsoulapiapp.login.serializers import MobileRegistrationSerializer
    serializer = MobileRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return custom_error_response(serializer)

    try:
        otp = generate_otp()
        current_local_time = get_current_time()

        # Update or create the MobileRegistration entry
        update_or_create_mobile_registration(received_mobile_no, str(otp), str(current_local_time))

        response_data = {"otp": otp, "message": "OTP is valid for only 2 minutes."}
        return create_response("Success", response_data, status_code=status.HTTP_200_OK)
    except Exception as e:
        return custom_error_response(str(e))


@api_view(["POST"])
def login_via_otp(request: Request) -> Response:
    """Handle requests to get OTP for a mobile number."""
    received_mobile_no = request.data.get("mobileNo")
    fcm_token = request.data.get("fcm_token")

    from rajneehsoulapiapp.login.serializers import GetOtpSerializer
    serializer = GetOtpSerializer(data=request.data)
    if not serializer.is_valid():
        return custom_error_response(serializer)

    # Retrieve the MobileRegistration object
    mobile_registration = get_object_or_404(MobileRegistration, mobileNo=received_mobile_no)

    # Update mobile registration details
    mobile_registration.otp = ""
    mobile_registration.fcm_token = fcm_token
    mobile_registration.save()

    # Generate token for the user after OTP validation

    # Check for existing AuthToken
    auth_token = AuthToken.objects.filter(user_id=mobile_registration.id).first()

    if auth_token:
        return handle_existing_token(auth_token, mobile_registration)
    else:
        # Ensure CustomUser is created and linked to the MobileRegistration
        custom_user = CustomUser.objects.filter(userMobileLinked=mobile_registration).first()

        if not custom_user:
            custom_user = CustomUser.objects.create(
                username=f"mobile_user_{received_mobile_no}",
                password="random_password",  # You can generate a random password or leave it empty if required
                userMobileLinked=mobile_registration
            )

        # Generate a new AuthToken
        return handle_new_token(mobile_registration, custom_user)

