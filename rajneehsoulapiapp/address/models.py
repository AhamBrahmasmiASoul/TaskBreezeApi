from django.db import models

# models.py
from django.core.exceptions import ValidationError

from rajneehsoulapiapp.login.models import EmailIdRegistration


def validate_pincode(value):
    if not value.isdigit() or len(value) != 6:
        raise ValidationError("Pincode must be exactly 6 digits.")

class Address(models.Model):
    pincode = models.CharField(max_length=6, validators=[validate_pincode])
    address = models.CharField(max_length=255)
    user = models.ForeignKey(EmailIdRegistration, on_delete=models.CASCADE, related_name="addresses")

