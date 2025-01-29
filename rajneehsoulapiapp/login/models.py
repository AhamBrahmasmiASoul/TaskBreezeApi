import re

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from rest_framework.exceptions import ValidationError

# Custom regex validator for email
def validate_email_regex(value):
    # Regular expression for validating an email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, value):
        raise ValidationError(f"Invalid email address: {value}")

class EmailIdRegistration(models.Model):
    emailId = models.EmailField(
        max_length=45,
        validators=[validate_email_regex],
        verbose_name="Email Address"
    )
    otpTimeStamp = models.CharField(max_length=100, default="")
    otp = models.CharField(max_length=100, default="")
    fcmToken = models.CharField(max_length=200, default="")
    objects = models.Manager()


class AuthToken(models.Model):
    user = models.ForeignKey(EmailIdRegistration, on_delete=models.CASCADE)
    key = models.CharField(verbose_name='Key', max_length=40)
    objects = models.Manager()


class CustomUser(AbstractUser):
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Specify a unique related_name
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Specify a unique related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    userMobileLinked = models.ForeignKey(EmailIdRegistration, on_delete=models.CASCADE, null=True)


from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class CustomUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(default=now)
    last_updated = models.DateTimeField(auto_now=True)
    is_premium_user = models.BooleanField(default=False)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
