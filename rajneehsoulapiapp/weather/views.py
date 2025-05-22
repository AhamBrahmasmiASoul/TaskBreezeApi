from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WeatherForecast, WeatherPincodeMappedData
from .serializers import WeatherForecastSerializer, WeatherPincodeMappedDataSerializer
from ..address.models import Address
from ..address.serializers import AddressSerializer
from ..schedule_list.models import ScheduleItemList
from ..schedule_list.serializers import ScheduleItemListSerializers


class WeatherForecastAPIView(APIView):

    def get(self, request):
        expired_param = request.query_params.get('expired')
        forecasts = WeatherForecast.objects.all()

        if expired_param == "false":
            current_time = now()
            forecasts = forecasts.filter(
                scheduleItem__dateTime__gt=current_time,
                isActive=True,
                scheduleItem__isWeatherNotifyEnabled=True
            )

        serializer = WeatherForecastSerializer(forecasts, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = WeatherForecastSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):

        forecast_id = request.query_params.get('forecast_id')

        try:
            instance = WeatherForecast.objects.get(id=forecast_id)
        except WeatherForecast.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WeatherForecastSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_count=instance.updated_count + 1)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Q, Prefetch

from django.db.models import Q


def weather_stats_view(request):
    query = request.GET.get("q", "").strip()
    weather_type = request.GET.get("weather_type", "").strip()
    pincode = request.GET.get("pincode", "").strip()
    is_active = request.GET.get("is_active", "").strip()  # NEW

    # Start by getting all forecasts
    forecasts = WeatherForecast.objects.filter(
        scheduleItem__isWeatherNotifyEnabled=True  # Filter by related ScheduleItem's isWeatherNotifyEnabled field
    ).order_by('-last_updated')
    # Apply filtering based on the search query
    if query:
        forecasts = forecasts.filter(
            Q(pincode__icontains=query) |
            Q(scheduleItemId__icontains=query) |
            Q(weatherType__icontains=query) |
            Q(weatherDescription__icontains=query)
        )

    if weather_type:
        forecasts = forecasts.filter(weatherType__icontains=weather_type)

    if pincode:
        forecasts = forecasts.filter(pincode__icontains=pincode)

    if is_active == "1":
        forecasts = forecasts.filter(isActive=True)
    elif is_active == "0":
        forecasts = forecasts.filter(isActive=False)

    # Apply the slicing after filtering
    forecasts = forecasts[:100]  # Latest 100 entries after filtering

    return render(request, "weather_stats.html", {
        "forecasts": forecasts,
        "query": query,
        "weather_type": weather_type,
        "pincode": pincode,
        "is_active": is_active,
    })


class WeatherPincodeMappedDataAPIView(APIView):

    def get(self, request, format=None):
        pincode = request.query_params.get('pincode')
        if pincode:
            instance = get_object_or_404(WeatherPincodeMappedData, pincode=pincode)
            serializer = WeatherPincodeMappedDataSerializer(instance)
            return Response(serializer.data)
        else:
            all_data = WeatherPincodeMappedData.objects.all()
            serializer = WeatherPincodeMappedDataSerializer(all_data, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WeatherPincodeMappedDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        pincode = request.query_params.get('pincode')
        if not pincode:
            return Response({'error': 'Pincode is required for PATCH'}, status=status.HTTP_400_BAD_REQUEST)

        instance = get_object_or_404(WeatherPincodeMappedData, pincode=pincode)
        serializer = WeatherPincodeMappedDataSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeatherScheduledData(APIView):
    def get(self, request, format=None):
        bulk_data = []
        user_info = None  # assume only one user context for now
        pincodes = set()  # to store unique pincodes

        # Get all schedule items where weather notification is enabled
        schedule_items = ScheduleItemList.objects.filter(
            isWeatherNotifyEnabled=True
        ).select_related('user')

        for schedule in schedule_items:
            user = schedule.user
            addresses = Address.objects.filter(user=user)

            # Serialize once per user
            if user_info is None:
                user_info = {
                    "id": user.id,
                    "emailId": user.emailId,
                    "fcmToken": user.fcmToken,
                    "otp": user.otp,
                    "otpTimeStamp": user.otpTimeStamp
                }

            schedule_serialized = ScheduleItemListSerializers(schedule).data

            for address in addresses:
                address_serialized = AddressSerializer(address).data
                pincode = address_serialized.get("pincode")

                if pincode:
                    pincodes.add(pincode)

                bulk_data.append({
                    "address": address_serialized,
                    "schedule_item": schedule_serialized
                })

        return Response({
            "bulk_data": bulk_data,
            "user_info": user_info,
            "pincodes": list(pincodes)  # convert set to list for JSON serialization
        })


