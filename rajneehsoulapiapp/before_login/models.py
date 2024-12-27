from enum import Enum

from django.db import models

class AppSpecificDetails(models.Model):
    language_code = models.IntegerField(default=0)
    theme = models.IntegerField(default=1)

    def __str__(self):
        return f"Language: {self.language_code}, Theme: {self.theme}"


class AppUpdateInfo(models.Model):
    redirect_url = models.URLField(blank=True, null=True)
    current_version = models.CharField(max_length=50, blank=True, null=True)
    update_mode = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Version: {self.current_version or 'Unknown'}"


class AppTourInfo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.title or "Untitled Tour"


class AppDetails(models.Model):
    app_specific_details = models.OneToOneField(AppSpecificDetails, on_delete=models.CASCADE, related_name="app_details")
    app_update_info = models.OneToOneField(AppUpdateInfo, on_delete=models.CASCADE, related_name="app_details")
    app_tour_info = models.ManyToManyField(AppTourInfo, related_name="app_details")

    def __str__(self):
        return f"AppDetails ID: {self.id}"


class MyModel(models.Model):
    class StatusEnum(Enum):
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"
    STATUS_CHOICES = [(status.value, status.name) for status in StatusEnum]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=StatusEnum.PENDING.value,
    )