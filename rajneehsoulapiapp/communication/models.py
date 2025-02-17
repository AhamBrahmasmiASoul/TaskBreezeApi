from django.db import models

class OtpConfig(models.Model):
    via_mail = models.BooleanField(default=False)

    def __str__(self):
        return f"Send OTP via Mail: {self.via_mail}"
