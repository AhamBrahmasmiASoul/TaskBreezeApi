from django.urls import path
from .views import SendEmailAPIView, SendWeatherNotificationAPIView

urlpatterns = [
    path('send-email/', SendEmailAPIView.as_view(), name='send-email'),
    path('send-weather-notify-email', SendWeatherNotificationAPIView.as_view(), name='send-weather-notify-email'),
]