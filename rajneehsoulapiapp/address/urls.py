# urls.py
from django.urls import path
from .views import AddressView

urlpatterns = [
    path('pincode', AddressView.as_view(), name='address-api'),
]