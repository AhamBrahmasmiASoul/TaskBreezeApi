from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.db import models

from rajneehsoulapiapp.login.models import EmailIdRegistration

class ItemType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ScheduleItemList(models.Model):
    user = models.ForeignKey(EmailIdRegistration, on_delete=models.CASCADE, related_name="user", null=True)
    google_auth_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="google_auth_user", null=True)
    dateTime = models.DateTimeField()
    title = models.CharField(max_length=1000, default="Title")
    isItemPinned = models.BooleanField(default=False)
    lastScheduleOn = models.CharField(default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%d-%m-%Y %I:%M:%S %p'),
                                      max_length=200)
    subTitle = models.CharField(max_length=1000, default="Sub Title")
    isArchived = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    isWeatherNotifyEnabled = models.BooleanField(default=False)

    objects = models.Manager()


class ScheduleListAttachments(models.Model):
    user = models.ForeignKey(
        ScheduleItemList,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='schedule_list/attachments/files/', blank=True, null=True)
