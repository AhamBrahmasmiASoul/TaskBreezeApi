from django.http import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import requests
from firebase_admin import *

from notification_utils import check_date_difference, find_datetime_range, format_date
from rajneehsoulapiapp.communication.mail import send_email_anonymous

class SendEmailAPIView(APIView):
    """
    API View to send a templated email to a user.
    """

    def get(self, request):
        email = request.query_params.get('email')  # Get email from query params
        if not email:
            return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user from the database
        user = User.objects.get(email=email)

        # Send email
        from rajneehsoulapiapp.communication.mail import send_email
        send_email(user)

        return Response({"message": f"Email sent successfully to {email}."}, status=status.HTTP_200_OK)

class SendWeatherNotificationAPIView(APIView):
    """
    API View to send a templated email to a user.
    """

    def post(self, request):
        data = request.data

        # Extract fields from request body
        email = data.get("emailId")
        schedule_date_time = data.get("schedule_date_time")
        task_name = data.get("task_name")
        weather_status = data.get("weather_status")

        # Validate required fields
        if not email or not task_name or not weather_status:
            return Response(
                {"error": "emailId, taskName, and weatherStatus are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Send the email
        try:
            send_email_anonymous(task_name, email, schedule_date_time, weather_status)
        except Exception as e:
            return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"message": f"Email sent successfully to {email}."},
            status=status.HTTP_200_OK
        )



