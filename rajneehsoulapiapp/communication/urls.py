from django.urls import path
from .views import SendEmailAPIView

urlpatterns = [
    path('send-email/', SendEmailAPIView.as_view(), name='send-email'),
]