from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from requests import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rajneehsoulapiapp.communication.mail import send_email_otp_verification
from rajneehsoulapiapp.communication.models import OtpConfig
from rajneehsoulapiapp.login.const import validity_period
from rajneehsoulapiapp.login.models import EmailIdRegistration, AuthToken, CustomUser
from rajneehsoulapiapp.login.utils.utillity import (
    handle_existing_token,
    handle_new_token,
    custom_error_response,
    create_response, update_or_create_email_id_registration, generate_otp, get_current_time,
)

def is_otp_sent_via_mail():
    """Fetch OTP configuration from the database."""
    config = OtpConfig.objects.first()  # Assuming only one config exists
    return config.via_mail if config else False  # Default to False if no entry


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
        current_local_time = get_current_time()

        # Update or create the MobileRegistration entry
        update_or_create_email_id_registration(received_email_id, str(otp), str(current_local_time))

        # Check if OTP should be sent via mail
        if is_otp_sent_via_mail():
            send_email_otp_verification(received_email_id, otp, validity_period)
            response_data = {"message": f"OTP sent via email to {received_email_id} successfully."}
        else:
            response_data = {"message":"Success", "otp" : otp}


        return create_response("Success", response_data, status_code=status.HTTP_200_OK)

    except Exception as e:
        return custom_error_response(str(e))


@api_view(["POST"])
def login_via_otp(request: Request) -> Response:
    """Handle requests to get OTP for a Email number."""
    received_email_id = request.data.get("emailId")
    entered_otp = request.data.get("otp")
    fcm_token = request.data.get("fcm_token")

    from rajneehsoulapiapp.login.serializers import GetOtpSerializer
    serializer = GetOtpSerializer(data=request.data)
    if not serializer.is_valid():
        return custom_error_response(serializer)

    # Retrieve the MobileRegistration object
    email_id_registration = get_object_or_404(EmailIdRegistration, emailId=received_email_id)

    # Validate OTP
    if email_id_registration.otp != str(entered_otp):
        return create_response("Error", {"message": "Invalid OTP."}, status_code=status.HTTP_400_BAD_REQUEST)

        # Check OTP expiry
    from datetime import datetime, timedelta, timezone

    if email_id_registration.otpTimeStamp:
        try:
            # Ensure OTP timestamp is timezone-aware
            otp_timestamp = datetime.fromisoformat(email_id_registration.otpTimeStamp)
            if otp_timestamp.tzinfo is None:  # Convert naive datetime to UTC
                otp_timestamp = otp_timestamp.replace(tzinfo=timezone.utc)

            # Get current time in UTC
            current_time = datetime.now(timezone.utc)

            # Normalize timestamps by removing microseconds
            otp_timestamp = otp_timestamp.replace(microsecond=0)
            current_time = current_time.replace(microsecond=0)

        except ValueError:
            return create_response("Error", {"message": "Invalid OTP timestamp format."},
                                   status_code=status.HTTP_400_BAD_REQUEST)

        print("current_time : ", current_time)
        print("otp_timestamp : ", otp_timestamp)
        print("timedelta(validity_period) : ", timedelta(minutes=validity_period))
        print("current_time > otp_timestamp + timedelta(validity_period) : ",
              current_time > otp_timestamp + timedelta(minutes=validity_period))

        if current_time > otp_timestamp + timedelta(minutes=validity_period):
            return create_response("Error", {"message": "OTP has expired."},
                                   status_code=status.HTTP_400_BAD_REQUEST)

    from datetime import datetime, timedelta, timezone

    if email_id_registration.otpTimeStamp:
        try:
            # Ensure OTP timestamp is timezone-aware
            otp_timestamp = datetime.fromisoformat(email_id_registration.otpTimeStamp)

            # Get current time in UTC
            current_time = datetime.now(timezone.utc)


            # Normalize timestamps by removing microseconds
            otp_timestamp = otp_timestamp.replace(microsecond=0)
            current_time = current_time.replace(microsecond=0)


        except ValueError:
            return create_response("Error", {"message": "Invalid OTP timestamp format."},
                                   status_code=status.HTTP_400_BAD_REQUEST)

        if current_time > otp_timestamp + timedelta(minutes=validity_period):
            return create_response("Error", {"message": "OTP has expired."},
                                   status_code=status.HTTP_400_BAD_REQUEST)

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
        custom_user = CustomUser.objects.filter(emailIdLinked=email_id_registration).first()

        if not custom_user:
            custom_user = CustomUser.objects.create(
                username=f"mobile_user_{received_email_id}",
                password="random_password",  # You can generate a random password or leave it empty if required
                emailIdLinked=email_id_registration
            )

        # Generate a new AuthToken
        return handle_new_token(email_id_registration, custom_user)

