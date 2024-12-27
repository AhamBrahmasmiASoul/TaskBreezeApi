from datetime import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Function to create JWT token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)  # This line should be updated
    access = AccessToken.for_user(user)  # Create the access token similarly
    return {
        'refresh': str(refresh),
        'access': str(access),
    }


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime('%Y-%m-%d %H:%M')  # Desired output format

    def to_internal_value(self, data):
        try:
            parsed_datetime = datetime.strptime(data, '%Y-%m-%d %H:%M')

            print("parsed_datetime : ", type(parsed_datetime))
            print("timezone.now() : ", type(timezone.now()))
            if timezone.make_aware(parsed_datetime, timezone.get_current_timezone()) <= timezone.now():
                raise serializers.ValidationError("Datetime cannot be in the past.")
            return parsed_datetime
        except ValueError:
            raise serializers.ValidationError("Invalid datetime format. Use 'YYYY-MM-DD HH:MM'.")