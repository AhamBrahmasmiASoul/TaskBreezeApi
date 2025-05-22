from django.urls import path
from .views import WeatherForecastAPIView, weather_stats_view, WeatherPincodeMappedDataAPIView, WeatherScheduledData

urlpatterns = [
    path("forecast", WeatherForecastAPIView.as_view(), name="weather-forecast"),
    path("forecast-stats/", weather_stats_view, name="weather_stats"),
    path("pincode-weather-mapping", WeatherPincodeMappedDataAPIView.as_view(), name="pincode_weather_data"),
    path("get-user-mapping", WeatherScheduledData.as_view(), name="get_user_mapping"),
]