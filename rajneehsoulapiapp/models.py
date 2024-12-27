from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=255, blank=True)
    sub_title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField()
    image = models.TextField(blank=True)
    imageViaUrl = models.ImageField(upload_to='images/', blank=True)
    subTitle = models.CharField(max_length=1000, default="Sub Title")
    isArchived = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.title or "Untitled"

