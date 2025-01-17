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

    # def get(self, request):
    #     email = request.query_params.get('email')  # Get email from query params
    #     if not email:
    #         return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # Fetch user from the database
    #     user = User.objects.get(email=email)
    #
    #     # Send email
    #     from rajneehsoulapiapp.communication.mail import send_email
    #     send_email(user)
    #
    #     return Response({"message": f"Email sent successfully to {email}."}, status=status.HTTP_200_OK)

    def get(self, request):
        email = request.query_params.get('email')  # Get email from query params
        if not email:
            return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Send email
        from rajneehsoulapiapp.communication.mail import send_email
        email = request.query_params.get('email')
        api_address = "https://api.openweathermap.org/data/2.5/forecast?appid=61d38a3c289f168e130b1fa745c9a37c&q="

        url = api_address + "Gurugram"

        json_data = requests.get(url).json()
        json_string = json.dumps(json_data, indent=4)
        data = json.loads(json_string)
        allowedList = []
        for i in range(len(data['list'])):
            weather_date_time = data['list'][i]['dt_txt']

            allowed_diff = check_date_difference(weather_date_time, "2025-01-19 12:00:00", "1 Day")
            if allowed_diff:
                print("info: ", weather_date_time)
                allowedList.append(data['list'][i])
                print("weather info : ", data['list'][i]["weather"][0]["description"])

        print("allowedList: ", allowedList)
        result = find_datetime_range(allowedList, "2025-01-19 00:00:00")

        from datetime import datetime

        # Convert to datetime object
        dt_obj = datetime.strptime(result["start_range"], "%Y-%m-%d %H:%M:%S")

        # Format the datetime object to the desired format
        formatted_date = dt_obj.strftime("%d %b, %Y %I:%M %p")

        send_email_anonymous(email, formatted_date, result["weather_info"])

        return Response({"message": f"Email sent successfully to {email}."}, status=status.HTTP_200_OK)




