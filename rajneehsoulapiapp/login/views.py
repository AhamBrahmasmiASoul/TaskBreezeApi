from django.shortcuts import get_object_or_404
from requests import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rajneehsoulapiapp.communication.mail import send_email_otp_verification
from rajneehsoulapiapp.login.models import EmailIdRegistration, AuthToken, CustomUser
from rajneehsoulapiapp.login.utils.utillity import (
    handle_existing_token,
    handle_new_token,
    custom_error_response,
    create_response, update_or_create_email_id_registration, generate_otp, get_current_time,
)


@api_view(["POST"])
def get_otp_api(request: Request) -> Response:
    """Handle mobile login requests."""
    received_email_id = request.data.get("emailId")
    if not received_email_id:
        return custom_error_response("Email number is required.")

    from rajneehsoulapiapp.login.serializers import MobileRegistrationSerializer
    serializer = MobileRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return custom_error_response(serializer)

    try:
        otp = generate_otp()
        validity_period = "2"
        current_local_time = get_current_time()

        # Update or create the MobileRegistration entry
        update_or_create_email_id_registration(received_email_id, str(otp), str(current_local_time))

        #send_email_otp_verification(received_email_id, otp, validity_period)

        #response_data = {"message": "OTP send on email : " + received_email_id + " successfully."}
        response_data = {"message": "OTP  : " + str(otp)}


        return create_response("Success", response_data, status_code=status.HTTP_200_OK)

    except Exception as e:
        return custom_error_response(str(e))


@api_view(["POST"])
def login_via_otp(request: Request) -> Response:
    """Handle requests to get OTP for a Email number."""
    received_email_id = request.data.get("emailId")
    fcm_token = request.data.get("fcm_token")

    from rajneehsoulapiapp.login.serializers import GetOtpSerializer
    serializer = GetOtpSerializer(data=request.data)
    if not serializer.is_valid():
        return custom_error_response(serializer)

    # Retrieve the MobileRegistration object
    email_id_registration = get_object_or_404(EmailIdRegistration, emailId=received_email_id)

    # Update mobile registration details
    email_id_registration.otp = ""
    email_id_registration.fcm_token = fcm_token
    email_id_registration.save()

    # Generate token for the user after OTP validation

    # Check for existing AuthToken
    auth_token = AuthToken.objects.filter(user_id=email_id_registration.id).first()

    if auth_token:
        return handle_existing_token(auth_token, email_id_registration)
    else:
        # Ensure CustomUser is created and linked to the MobileRegistration
        custom_user = CustomUser.objects.filter(userMobileLinked=email_id_registration).first()

        if not custom_user:
            custom_user = CustomUser.objects.create(
                username=f"mobile_user_{received_email_id}",
                password="random_password",  # You can generate a random password or leave it empty if required
                userMobileLinked=email_id_registration
            )

        # Generate a new AuthToken
        return handle_new_token(email_id_registration, custom_user)

