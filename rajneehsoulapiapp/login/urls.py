from django.urls import path

from rajneehsoulapiapp.login import views

urlpatterns = [
    path("get-otp", views.get_otp_api, name="get-otp"),
    path("login-via-otp", views.login_via_otp, name="login-via-otp"),
]
